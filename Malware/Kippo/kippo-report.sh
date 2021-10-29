#!/bin/bash
# Simple Kippo stats reporting script

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

echo "Kippo Summary"
echo "Reporting Period: ${START} - ${STOP}"
echo
echo -n "Total sessions: "
grep "session: " ${LOGFILE} | wc -l

echo -n "Successful logins: "
grep "login attempt" ${LOGFILE} | grep succeeded | wc -l
echo

echo -n "Total unique failed usernames: "
grep "login attempt" ${LOGFILE} | grep failed | cut -d\/ -f 1 | cut -d \[ -f3 | sort | uniq | wc -l
echo

echo "Failed usernames with frequency"
echo "-------------------------------"
grep "login attempt" ${LOGFILE} | grep failed | cut -d\/ -f 1 | cut -d \[ -f3 | sort | uniq > /tmp/fusers
for x in `cat /tmp/fusers`
 do
  echo -n "${x}: "
  grep "login attempt" ${LOGFILE} | grep failed | grep ${x} | cut -d\/ -f 1 | cut -d \[ -f3 | sort | uniq | wc -l
done
rm /tmp/fusers
echo

echo "Failed Username and Password Combinations"
echo "------------------------------------------"
grep "login attempt" ${LOGFILE} | grep failed | cut -d\[ -f 3| cut -f1 -d \] | sort | uniq
echo

echo "Successful Usernames with frequency: "
echo "-------------------------------------"
grep "authenticated with" ${LOGFILE} | awk -F" "  '{print $7}' | sort | uniq > /tmp/users
grep "authenticated with" ${LOGFILE} > /tmp/sessions
for x in `cat /tmp/users` 
 do echo -n "${x}: " 
  grep ${x} /tmp/sessions | wc -l 
done
rm /tmp/users /tmp/sessions
echo

echo "Passwords used in successful logins"
echo "-----------------------------------"
grep succeeded ${LOGFILE} | cut -f 2 -d\/ | cut -f 1 -d \] | sort | uniq > /tmp/passes
for x in `cat /tmp/passes`
 do
  echo -n "${x}: "
  grep ${x} ${LOGFILE} | grep succeeded | wc -l
done
echo "-----------------------------------"
rm /tmp/passes
echo

echo "Actual interactive sessions"
echo "--------------------------"
grep "Opening TTY log" ${LOGFILE} | awk -F"," '{ print $3 }' | awk -F"]" '{ print $1 }' > /tmp/sessip
for x in `cat /tmp/sessip` 
 do 
  echo "${x}: " 
  echo "-------------------"
  DATE=`grep ${x} ${LOGFILE} | grep "Opening TTY log" | awk -F" " '{ print $1 " " $2}' | sort | uniq ` 
  BLAH=`grep "Opening TTY log" ${LOGFILE} | grep $x | awk -F" " '{ print "/home/matt/kippo/kippo-0.8/"$14 }' `
  SIZE=`ls -lh ${BLAH} | awk -F" " '{ print $5 }'`
  LOG=`grep ${x} ${LOGFILE} | grep "Opening TTY log" | awk -F":" '{ print $4 }' `
  echo "${DATE}: ${LOG} (${SIZE})"
  echo ""
done
rm /tmp/sessip
echo

echo "Downloaded files"
echo "--------------------------"
echo
grep "Starting factory <HTT" ${LOGFILE} | awk -F"," '{ print $3 }' | awk -F"]" '{ print $1 }' > /tmp/dlip
for x in `cat /tmp/dlip`
 do 
  echo -n "${x}: "
  grep ${x} ${LOGFILE} | grep "Starting factory <HTT" | awk -F" " '{ print $14 }' | awk -F">" '{ print $1 }'
done
rm /tmp/dlip
echo
