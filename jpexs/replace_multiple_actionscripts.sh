#!/usr/bin/env bash

set -e

touch ./output.swf
echo -e "\nReplacing scripts for $1...\n"
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v "$2:/scripts" -v ./output.swf:/output.swf jpexs \
    -replace /file.swf /output.swf "${@:3}"
