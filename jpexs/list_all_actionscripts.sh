#!/usr/bin/env bash

set -e

docker run -u 1000:1000 --rm -it -v ./$1:/file.swf jpexs -dumpAS2 /file.swf
