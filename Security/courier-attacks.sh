#!/bin/bash
# Simple script to parse the Exim reject log and pull some naughty stats

LOGFILE="/var/log/exim4/rejectlog"
ATTACKERS="/tmp/.attackers"
USERS="/tmp/.users"
REGEX="Incorrect"
DUMPREPORT="./attacker-report.txt"


function attackersummary() {
echo "Attacker Summary"
echo "---------------------------------------"
for x in `cat ${ATTACKERS}` 
 do 
   echo -n "${x}: " 
    grep ${REGEX} ${LOGFILE} | grep -e "${x}" | awk -F"=" ' { print $2} ' | awk -F")" '{ print $1 }'  | wc -l 
done
echo "---------------------------------------"
 }

function summaryquery() {
echo -n "Print username summary Y/N? "
read ANSWER
if [ ${ANSWER} == "y" ]; then
		usersummary
else
        dumpreport
		# Clean up
		rm ${ATTACKERS} ${USERS}
		echo "Exiting"
		exit 0
fi
}

function usersummary() {
		echo "Attacker username summary"
		echo "---------------------------------------"
		for x in `cat ${ATTACKERS}` 
		 do 
		  grep ${REGEX} ${LOGFILE} | grep -w "${x}" > /tmp/${x}-attack_summary.txt
		  echo "Attacker: ${x}" 
		  for y in `cat ${USERS}`
		   do 
			 ATTACKS=`grep -w "${y}" /tmp/${x}-attack_summary.txt | awk -F"=" ' { print $2} ' | awk -F")" '{ print $1 }' | wc -l`
			 if [ ${ATTACKS} == "0" ];
			 then 
			   continue
			 else
			  echo -n "${y}: "
			  echo ${ATTACKS}
			 fi
		  done
		  echo "---------------------------------------"
		 rm /tmp/${x}-attack_summary.txt
		done
}

function dumpreport() {
echo -n "Dump report to file ? Y/N "
read ANSWER
if [ ${ANSWER} = "y" ] 
 then
  echo "Dumping: ${DUMPREPORT}"
  usersummary > ${DUMPREPORT}
else
 echo "We're done here."
 exit 0
fi
}

echo "Getting stats"
cat ${LOGFILE} | grep ${REGEX} | awk -F"[" '{ print $2 }' | awk -F"]" '{ print $1}' | sort| uniq > ${ATTACKERS}
cat ${LOGFILE} | grep ${REGEX} | awk -F"=" ' { print $2} ' | awk -F")" '{ print $1 }' | sort | uniq > ${USERS}

attackersummary
summaryquery
dumpreport
  
echo "Report complete"

