#!/usr/bin/env bash

target=${1%/}
dest_input=${2-"."}
dest=${dest_input%/}
full_target=$(readlink -f $target)
echo "Version to promote: $target/"
rsync -avh --link-dest=$full_target $target/ $dest/media/
