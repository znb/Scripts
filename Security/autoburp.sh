#!/bin/bash

JAVA="/usr/bin/java"
BURPPATH="/root/tools-proxies/burpsuite"
BURPSUITE="burpsuite_pro_v1.6.jar"
OPTIONS="-Djava.awt.headless=true -Xmx2g"
SCHEME=$1
TARGET=$2
PORT=$3
OUTPUTDIR=$4

if [[ -n $1 && -n $2 && -n $3 ]]
 then
   echo "Scanning: ${TARGET}:${PORT}"
   echo "Output: ${OUTPUTDIR}"
   ${JAVA} ${OPTIONS} -jar ${BURPPATH}/${BURPSUITE}  ${SCHEME} ${TARGET} ${PORT} ${OUTPUTDIR}
else
  echo "Usage: $0 scheme fqdn port output"
  echo "Example: $0 http www.example.com 80 /tmp/reportdir"
  exit
fi
