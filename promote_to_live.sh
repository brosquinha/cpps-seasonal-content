#!/usr/bin/env bash

target=${1%/}
echo "Version to promote: $target/"
rsync -avh --link-dest=$(pwd)/$target $target/ media/
