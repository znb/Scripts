#!/bin/bash
# Simple Glastopf stats reporting script

LOGFILE="${1}"

if [ "${LOGFILE}" = "" ]  
 then
  echo "We need a log file"
  exit 0
fi

if [ -f $LOGFILE ]
 then 
  true
else 
  echo "Log file doesn't exist"
  exit 0
fi

START=`head -1 ${LOGFILE} | awk -F" " '{print $1" " $2}'`
STOP=`tail -1 ${LOGFILE} | awk -F" " '{print $1" " $2}'`

echo "Glastopf Summary Report"
echo "Reporting Period: ${START} - ${STOP}"
echo "----------------------------------------"
echo
echo -n "Total sessions: "
grep "requested " ${LOGFILE} | wc -l
echo

echo  "Offenders"
echo "----------"
cat ${LOGFILE} | cut -d ' ' -f 4 | sort | uniq > /tmp/attackers
for x in `cat /tmp/attackers`
 do
  echo -n "${x}: "
  grep ${x} ${LOGFILE} | grep requested | wc -l
done
rm /tmp/attackers
echo

echo "Requested URLs"
echo "---------------"
cat ${LOGFILE} | cut -d ' ' -f 4,6,7
echo

