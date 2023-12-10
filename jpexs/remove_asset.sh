#!/usr/bin/env bash

set -e

touch ./output.swf
ASSET_ID=$2
echo -e "\nRemoving $ASSET_ID...\n"
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v ./output.swf:/output.swf jpexs \
    -remove /file.swf /output.swf $ASSET_ID
