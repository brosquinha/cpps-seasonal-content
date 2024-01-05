import json
import subprocess
import os
from argparse import ArgumentParser
from datetime import datetime

def main(schedule_path: str, legacy_media_path: str):
    legacy_media_path = os.path.realpath(legacy_media_path)
    with open(schedule_path) as f:
        schedules = json.load(f)
    
    restore_base(legacy_media_path)
    deploy_catalogs(legacy_media_path, schedules['catalogs'])
    deploy_rooms(legacy_media_path, schedules['rooms'])
    deploy_events(legacy_media_path, schedules['events'])
    deploy_parties(legacy_media_path, schedules['parties'])
    
def restore_base(legacy_media_path: str):
    deploy_version(legacy_media_path, os.path.join(legacy_media_path, "media_original"))
    deploy_version(legacy_media_path, os.path.join(legacy_media_path, "base"))
    
def deploy_version(legacy_media_path: str, version_path: str):
    if not os.path.isabs(legacy_media_path) or not os.path.isabs(version_path):
        raise Exception("Expected absolute paths")
    legacy_media_path = os.path.normpath(legacy_media_path)
    version_path = os.path.normpath(version_path)
    print('Deploying', version_path)
    
    # rsync -avh --link-dest=$(pwd)/$target $target/ media/
    subprocess.run(["rsync", "-avh", f"--link-dest={version_path}",
                    f'{version_path}{os.sep}',
                    os.path.join(legacy_media_path, "media/")], check=True)

def deploy_catalogs(legacy_media_path: str, all_catalogs: dict):
    for catalog_type, catalogs in all_catalogs.items():
        if not catalogs:
            continue
        years = len(set([x["start_at"][0] for x in catalogs]))
        catalog = next((catalogs[i-1] for i, x in enumerate(catalogs) if compare_now(x['start_at'], years=years) > 0), catalogs[-1])
        deploy_version(legacy_media_path, os.path.join(legacy_media_path, "catalogs", catalog_type, catalog["name"], "media"))
    
def compare_now(relative_date: list[int], years: int) -> int:
    if len(relative_date) != 3:
        raise Exception("Invalid relative_date")
    now = datetime.utcnow()
    now_tuple = [now.year % years, now.month, now.day]
    
    for d, n in zip(relative_date, now_tuple):
        if d != n:
            return 1 if d > n else -1
    return 0

def deploy_rooms(legacy_media_path: str, rooms: list[dict]):
    pass

def deploy_events(legacy_media_path: str, events: list[dict]):
    pass

def deploy_parties(legacy_media_path: str, parties: list[dict]):
    years = len(set([x["start_at"][0] for x in parties]))
    party = next((x for x in parties if compare_now(x['start_at'], years=years) <= 0 and compare_now(x['end_at'], years=years) >= 0), None)
    if party:
        deploy_version(legacy_media_path, os.path.join(legacy_media_path, "parties", party["name"], "media"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("schedule_path")
    parser.add_argument("legacy_media_path")
    args = parser.parse_args()
    
    main(args.schedule_path, args.legacy_media_path)
