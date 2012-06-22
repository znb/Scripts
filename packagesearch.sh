#!/bin/bash
# simple package search tool to grab the version info 
# of a debian package. 
# code at zonbi dot org

while true
 do
        echo -n "app> "
        read APP
        echo -n "$APP "
        apt-cache show $APP | grep -e "Version:" | awk -F" " '{ print $2 }'
done