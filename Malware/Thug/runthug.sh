#!/bin/bash

# version 0.1
# todo: add tor support

URL=$1
BROWSERS="winxpie60 winxpie61 winxpie70 winxpie80 winxpchrome20 winxpfirefox12 winxpsafari5 win2kie60 win2kie80 win7ie80 win7ie90 win7chrome20 win7safari5 osx10safari5 osx10chrome19"
THUGDIR=/home/matt/thug/thug/src
THUGOUT=/home/matt/thug_out

echo "Scanning url: $1"

cd $THUGDIR
for x in $BROWSERS
 do
  echo "Running scan with $x"
  python ./thug.py -u $x -n $THUGOUT/$1-$x $1
  echo ""
  echo "sleeping"
  sleep 60
done