#!/bin/bash
# Master script for Thugdor
set -o nounset
set -o errexit

# TARGET
TARGET=$1

# CONFIGURATION
#
DATE=`date +%d_%m_%Y`
PYTHON="/usr/bin/python"
# OUTPUT DIRECTORIES
HOMEDIR="/home/matt"
REPORTDIR="${HOMEDIR}/Reports"
THUGREPORTS="${REPORTDIR}/Thug"
EYEWITNESS="${REPORTDIR}/Eyewitness"
URLLIST="${REPORTDIR}/checks.txt"
URLDUMPS="${REPORTDIR}/url_dumps"
TMPTHUGREPORTS="/tmp/thug-reports-$$.txt"
THUGPARSEOUTPUT="${REPORTDIR}/for-google-lookups.txt"
OUTPUTDIR="${HOMEDIR}/Output"
GOOGLESAFEIN="${OUTPUTDIR}/urls-for-lookup.txt"
EYEWITNESSIN="${OUTPUTDIR}/eyewitness.txt"
CHECKTHUG="/tmp/.thugme.txt"
REPORTFILE="${REPORTDIR}/thugdor-report-${DATE}.txt"
# SCRIPTS
SPIDER="${HOMEDIR}/Github/Malware/Thug/spider.py"
URLDUMPER="${HOMEDIR}/Github/Malware/Thug/url-dumper.py"
THUGPARSE="${HOMEDIR}/Github/Malware/Thug/thug-parse.py"
GOOGLELOOKUP="${HOMEDIR}/Github/Malware/Google/google-safe-lookup.py"
EYEWITNESS="${HOMEDIR}/Github/EyeWitness/EyeWitness.py"
# THUG AND OPTIONS
THUG="/opt/tools/thug/src/thug.py"
THUGUA="win7ie90"
THUGOPTS="-q -y"
THUGTIMEOUT="10"
THUGANALYSIS="analysis.json"


echo "" > ${REPORTFILE}
echo "[ Thugdor v0.1 ]" | tee -a ${REPORTFILE}
echo | tee -a ${REPORTFILE}

function spider {
    echo -n " * Running Spider" | tee -a ${REPORTFILE}
    ${PYTHON} ${SPIDER} -u ${TARGET} -f ${URLLIST} | tee -a ${REPORTFILE}
    echo | tee -a ${REPORTFILE}
}

function urldump {
    echo -n " * Running URL Dump script for Thug analysis" | tee -a ${REPORTFILE}
    test -d ${URLDUMPS} && true || mkdir -p ${URLDUMPS} 
    ${PYTHON} ${URLDUMPER} -f ${URLLIST} -d ${URLDUMPS} | tee -a ${REPORTFILE}
    echo | tee -a ${REPORTFILE}
}

function checkthug {
    test -f ${CHECKTHUG} && echo "Running Thug" && thuganalize || cleanup
}

function thuganalize {
    echo -n " * Running Thug on local files" | tee -a ${REPORTFILE}
    for URL in ${URLDUMPS}/*-SCANME 
	do 
	    ${PYTHON} ${THUG} -u ${THUGUA} ${THUGOPTS} -T ${THUGTIMEOUT} \
	    -n ${THUGREPORTS}/${URL} -l ${URL} | tee -a ${REPORTFILE}
	    CHOPPED=`basename ${URL} -SCANME`
	    mv ${URL} ${URLDUMPS}/${CHOPPED}-SCANNED
    done
    echo | tee -a ${REPORTFILE}
    thugparse
}

function thugparse {
    echo -n " * Running Thug parsing script on Thug reports" | tee -a ${REPORTFILE}
    find ${THUGREPORTS} -name ${THUGANALYSIS} >> ${TMPTHUGREPORTS}
    for THUG in `cat ${TMPTHUGREPORTS}`
	do
	    ${PYTHON} ${THUGPARSE} -r ${THUG} -n -o ${OUTPUTDIR} | tee -a ${REPORTFILE}
    done
    echo | tee -a ${REPORTFILE}
	googlelookup
}

function googlelookup {
	echo -n " * Running Google Safe Browsing Checks" | tee -a ${REPORTFILE}
	${GOOGLELOOKUP} -f ${GOOGLESAFEIN} -q
	eyewitness
}

function eyewitness {
    echo -n " * Running Eyewitness on any malicious links found" | tee -a ${REPORTFILE}
    test -d ${EYEWITNESSIN} &&  ${EYEWITNESS} --skipcreds --useragent \
	"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
	-t 10 -f ${EYEWITNESSIN} | tee -a ${REPORTFILE} \
	|| echo " [ No malicious links to grab ] " | tee -a ${REPORTFILE}
    echo | tee -a ${REPORTFILE}
    cleanup
}

function cleanup {
    echo ""
    echo "[ Complete ${DATE} ]" | tee -a ${REPORTFILE}
    rm -f ${TMPTHUGREPORTS} > /dev/null 2>&1
    rm -fr ${THUGREPORTS}/* > /dev/null 2>&1
    rm -fr ${HOMEDIR}/logs > /dev/null 2>&1
    rm -f ${CHECKTHUG} > /dev/null 2>&1
}

# The party starts here
spider
urldump
checkthug

