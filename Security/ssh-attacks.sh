#!/bin/bash
# Simple script to parse the auth log and pull some naughty stats

LOGFILE="/var/log/auth.log"
BADREGEX="Failed password for invalid"
GOODREGEX="Failed password for "
PASSWORDREGEX="Accepted password for"
PUBKEYREGEX="Accepted publickey for"

echo "Getting stats"
echo 

echo "Usernames in use"
echo "-----------------"
grep "${BADREGEX}" ${LOGFILE} | awk -F" " '{ print $11 }' | sort | uniq
echo "-----------------"
echo 

echo "Attackers"
echo "-----------------"
grep "${BADREGEX}" ${LOGFILE} | awk -F" " '{ print $13 }' | sort | uniq
echo "-----------------"
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
