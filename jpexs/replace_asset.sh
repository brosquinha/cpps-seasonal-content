#!/usr/bin/env bash

set -e

touch ./output.swf
ASSET_ID=$3
echo -e "\nReplacing $ASSET_ID...\n"
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v ./$2:/asset -v ./output.swf:/output.swf jpexs \
    -replace /file.swf /output.swf $ASSET_ID /asset
