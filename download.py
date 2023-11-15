import json
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

def main(assets_source_file):
    with open(assets_source_file) as f:
        assets = json.load(f)
        
    target_path = assets['target_path']
    arguments = [(x['url'], target_path, x['filename']) for x in assets['assets']]
        
    Pool(12).starmap(download_from_url, arguments)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("assets_file_path")
    args = parser.parse_args()
    
    main(args.assets_file_path)
