#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(dirname $0)
START_X_REGEX='^.*\.Startx\s*=\s*([0-9]+).*$'
START_Y_REGEX='^.*\.Starty\s*=\s*([0-9]+).*$'

$SCRIPT_DIR/extract_actionscript.sh $1

START_X=$(sed -En "s/$START_X_REGEX/\1/p" ./DoAction.as)
START_Y=$(sed -En "s/$START_Y_REGEX/\1/p" ./DoAction.as)

echo "Startx: '$START_X'"
echo "Starty: '$START_Y'"

cp ./assets/handcrafted/as1_fix.as ./DoAction.as

sed -iE "s/var start_x = 0;/var start_x = $START_X;/" ./DoAction.as
sed -iE "s/var start_y = 0;/var start_y = $START_Y;/" ./DoAction.as

touch ./output.swf
docker run -u 1000:1000 --rm -it -v ./$1:/file.swf -v ./output.swf:/output.swf jpexs -header -set version 9 /file.swf /output.swf
mv ./output.swf $1

$SCRIPT_DIR/replace_actionscript.sh $1 ./DoAction.as
