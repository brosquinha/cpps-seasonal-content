import os
from argparse import ArgumentParser


def main(legacy_media_path: str):
    valid_targets = []
    for root, dirs, files in os.walk(legacy_media_path):
        if dirs == ['media']:
            valid_targets.append(os.path.join(root, 'media'))
            
    print('\n'.join(sorted(valid_targets)))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("legacy_media_path")
    args = parser.parse_args()
    
    main(args.legacy_media_path)
