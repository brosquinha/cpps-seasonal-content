#!/usr/bin/env bash

set -e

touch ./output.swf
DEFAULT_SCRIPT_NAME=$(docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v ./$2:/DoAction.as -v ./output.swf:/output.swf jpexs -dumpAS2 /file.swf | tail -n 1)
SCRIPT_NAME=${3-${DEFAULT_SCRIPT_NAME%?}}
echo -e "\nReplacing $SCRIPT_NAME...\n"
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v ./$2:/DoAction.as -v ./output.swf:/output.swf jpexs \
    -replace /file.swf /output.swf "$SCRIPT_NAME" /DoAction.as
