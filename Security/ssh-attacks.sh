#!/bin/bash
# Simple script to parse the auth log and pull some naughty stats

LOGFILE="/var/log/auth.log"
REGEX="Failed password for invalid user"


echo "Getting stats"

echo "Usernames in use"
echo "-----------------"
grep "${REGEX}" ${LOGFILE} | awk -F" " '{ print $11 }' | sort | uniq
echo "-----------------"

echo "Attackers"
echo "-----------------"
grep "${REGEX}" ${LOGFILE} | awk -F" " '{ print $13 }' | sort | uniq
echo "-----------------"

echo "Successful Password Logins"
echo "--------------------------"
grep "Accepted password for" ${LOGFILE} | awk -F" " '{ print "Date: " $1" "$2" "$3 " IP: " $11" User: " $9 }'
echo "--------------------------"

echo "Successful Public Key Logins"
echo "----------------------------"
grep "Accepted publickey for" ${LOGFILE} | awk -F" " '{ print "Date: " $1" "$2" "$3 " IP: " $11" User: " $9 }'
echo "----------------------------"
