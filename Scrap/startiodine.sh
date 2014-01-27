#!/bin/bash

PASSWORD="yoursupersecret99charpassword"
NS="your.tunnelserver.org"
IPRANGE="10.0.0.1"

function bindcheck {
                BCHK=`pgrep -lf bind | wc -l`
                 if [ "${BCHK}" -gt "0" ];
                                then
                                                echo "Bind already running."
                                                echo "Kill Bind please"
                                                exit 0
                fi

}

echo "Checking for Bind"
bindcheck

echo "Starting iodine"
iodined -f -c -P ${PASSWORD} ${IPRANGE} ${NS}
