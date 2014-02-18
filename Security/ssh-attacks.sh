#!/bin/bash
# Simple script to parse the auth log and pull some naughty stats

LOGFILE="/var/log/auth.log"
BADREGEX="Failed password for invalid"
GOODREGEX="Failed password for "
PASSWORDREGEX="Accepted password for"
PUBKEYREGEX="Accepted publickey for"

echo "Getting stats"
echo 

echo -n "Total attacks: "
grep "${BADREGEX}" ${LOGFILE} | wc -l
echo -n "Total successful logins: "
grep "${PASSWORDREGEX}" ${LOGFILE} | wc -l > /tmp/.totpass
grep "${PUBKEYREGEX}" ${LOGFILE} | wc -l >> /tmp/.totpub
TOTPASS=`cat /tmp/.totpass`
TOTPUB=`cat /tmp/.totpub`
TOTAL=`expr ${TOTPASS} + ${TOTPUB}`
rm /tmp/.totpass /tmp/.totpub
echo ${TOTAL}
echo -n "Total good(ish) failed logins: "
grep "${GOODREGEX}" ${LOGFILE} | grep -v "invalid" | wc -l
echo

echo "Usernames in use"
echo "-----------------"
grep "${BADREGEX}" ${LOGFILE} | awk -F" " '{ print $11 }' | sort | uniq > /tmp/.users
for x in `cat /tmp/.users`
 do 
  echo -n "${x}: "
  grep "${BADREGEX}" ${LOGFILE} | grep -w "${x}" | wc -l
done
rm /tmp/.users
echo "-----------------"
echo 

echo "Attackers (with attacks)"
echo "------------------------"
grep "${BADREGEX}" ${LOGFILE} | awk -F" " '{ print $13 }' | sort | uniq > /tmp/.attackers
for x in `cat /tmp/.attackers`
 do
  echo -n "${x}: "
  grep ${x} ${LOGFILE} | grep "${BADREGEX}" | wc -l
done
rm /tmp/.attackers
echo "------------------------"
echo 

echo "Failed logins from good users"
echo "--------------------------"
grep "${GOODREGEX}" ${LOGFILE} | grep -v "invalid" | awk -F" " '{ print "Date: " $1" "$2" "$3 " IP: " $11" User: " $9 }'
echo "--------------------------"
echo 

echo "Successful Password Logins"
echo "--------------------------"
grep "${PASSWORDREGEX}" ${LOGFILE} | awk -F" " '{ print "Date: " $1" "$2" "$3 " IP: " $11" User: " $9 }'
echo "--------------------------"
echo

echo "Successful Public Key Logins"
echo "----------------------------"
grep "${PUBKEYREGEX}" ${LOGFILE} | awk -F" " '{ print "Date: " $1" "$2" "$3 " IP: " $11" User: " $9 }'
echo "----------------------------"
echo
