#!/bin/bash
# Simple script to parse the Exim reject log and pull some naughty stats

LOGFILE="/var/log/exim4/rejectlog"
ATTACKERS="/tmp/.attackers"
USERS="/tmp/.users"
REGEX="Incorrect"



echo "Getting stats"
cat ${LOGFILE} | grep ${REGEX} | awk -F"[" '{ print $2 }' | awk -F"]" '{ print $1}' | sort| uniq > ${ATTACKERS}
cat ${LOGFILE} | grep ${REGEX} | awk -F"=" ' { print $2} ' | awk -F")" '{ print $1 }' | sort | uniq > ${USERS}

echo "Attacker Summary"
echo "---------------------------------------"
for x in `cat ${ATTACKERS}` 
 do 
   echo -n "${x}: " 
    grep ${REGEX} ${LOGFILE} | grep -e "${x}" | awk -F"=" ' { print $2} ' | awk -F")" '{ print $1 }'  | wc -l 
done
echo "---------------------------------------"


echo -n "Print username summary Y/N? "
read ANSWER
if [ $ANSWER == "y" ]; then
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
else
		# Clean up
		rm ${ATTACKERS} ${USERS}
		echo "Exiting"
		exit 0
fi


