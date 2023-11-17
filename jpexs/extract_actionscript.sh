#!/usr/bin/env bash

set -e

OUTPUT_PATH=/tmp/ffdec_scripts
mkdir -p $OUTPUT_PATH
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v $OUTPUT_PATH:/output jpexs -export script /output /file.swf
mv $OUTPUT_PATH/scripts/frame_1/DoAction.as .
rm -rf $OUTPUT_PATH
