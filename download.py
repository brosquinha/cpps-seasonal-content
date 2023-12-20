import json
import subprocess
import time
import os
from argparse import ArgumentParser
from multiprocessing.dummy import Pool
from urllib.request import build_opener, install_opener, urlretrieve
from urllib.error import ContentTooShortError, HTTPError


def download_from_url(url: str, base_path: str, filename: str=None, retry: int=0):
    if not filename:
        filename = url.split('/')[-1]
    path = os.path.join(base_path, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f'Downloading {filename} to {path}...')
    
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    
    try:
        urlretrieve(url, path)
    except ContentTooShortError:
        download_from_url(url, base_path, filename)
    except HTTPError as e:
        if retry > 3:
            print(f'Retries maxed out for {filename}!')
            raise e
        retry += 1
        sleep = 2*retry
        time.sleep(sleep)
        print(f'Retrying {filename} in {sleep} seconds...')
        download_from_url(url, base_path, filename, retry=retry)
    except Exception as e:
        print(f'Failed to download {filename}!')
        raise e

def run_post_scripts(assets: dict):
    post_scripts: dict = assets.get('post_scripts', {})
    fix_as1_rooms(assets['target_path'], post_scripts.get('as1_rooms', []))
    apply_hard_links(assets['target_path'], post_scripts.get('hard_links', []))
    apply_actionscript_patches(assets['target_path'], post_scripts.get('actionscript_patches', []))
    apply_swf_replacements(assets['target_path'], post_scripts.get('swf_replacements', []))
    apply_swf_removals(assets['target_path'], post_scripts.get('swf_removals', []))
    
def fix_as1_rooms(base_path: str, filenames: list[str]):
    for filename in filenames:
        print(f'Fixing AS1 room {filename}')
        path = os.path.join(base_path, filename)
        subprocess.run(["./jpexs/fix_as1_room.sh", path], check=True, capture_output=True)
        os.replace("./output.swf", path)
    if os.path.exists("./DoAction.as"):
        os.remove("./DoAction.as")

def apply_hard_links(base_path: str, hard_links: list):
    print("Applying hard links")
    for [hard_link_target, hard_link_name] in hard_links:
        hard_link_src_path = os.path.join(base_path, hard_link_target)
        hard_link_dst_path = os.path.join(base_path, hard_link_name)
        os.makedirs(os.path.dirname(hard_link_dst_path), exist_ok=True)
        if os.path.exists(hard_link_dst_path):
            os.remove(hard_link_dst_path)
        os.link(hard_link_src_path, hard_link_dst_path)

def apply_actionscript_patches(base_path: str, as_patches: list[dict]):
    for patch in as_patches:
        print(f'Applying patch {os.path.basename(patch["patch_filename"])}')
        path = os.path.join(base_path, patch['target_filename'])
        script_path_source = patch.get('script_path', {}).get('source')
        script_path_target = patch.get('script_path', {}).get('target')
        subprocess.run(
            ["./jpexs/extract_actionscript.sh", path] + ([script_path_source] if script_path_source else []),
            check=True, capture_output=True)
        subprocess.run(
            ["patch", "DoAction.as", patch['patch_filename']],
            check=True, capture_output=True)
        subprocess.run(
            ["./jpexs/replace_actionscript.sh", path, "DoAction.as"] + ([script_path_target] if script_path_target else []),
            check=True, capture_output=True)
        os.replace("./output.swf", path)
    if os.path.exists("./DoAction.as"):
        os.remove("./DoAction.as")
    
def apply_swf_replacements(base_path: str, swf_replaces: list[dict]):
    for item in swf_replaces:
        print(f'Replacing assets for {item["swf_filename"]}')
        path = os.path.join(base_path, item["swf_filename"])
        for replacement in item["replacements"]:
            subprocess.run(
                ["./jpexs/replace_asset.sh", path, replacement["asset_filename"], str(replacement["id"])] ,
            check=True, capture_output=True)
            os.replace("./output.swf", path)
            
def apply_swf_removals(base_path: str, swf_removals: list[dict]):
    for item in swf_removals:
        print(f'Removing assets for {item["swf_filename"]}')
        path = os.path.join(base_path, item["swf_filename"])
        subprocess.run(
            ["./jpexs/remove_asset.sh", path, " ".join([str(x) for x in item["removals"]])],
            check=True, capture_output=True)
        os.replace("./output.swf", path)

def main(assets_source_file):
    with open(assets_source_file) as f:
        assets = json.load(f)
        
    target_path = assets['target_path']
    arguments = [(x['url'], target_path, x['filename']) for x in assets['assets']]
        
    Pool(12).starmap(download_from_url, arguments)
    run_post_scripts(assets)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("assets_file_path")
    args = parser.parse_args()
    
    main(args.assets_file_path)
