#!/usr/bin/python
# Simple script to detect if a domain/ip is malicious

import os
import argparse
import sys
try:
    import requests
except:
    print "You need python requests"


def load_apikey():
    """Load our API key from file"""
    fullpath = os.getenv("HOME")
    try:
        keyfile = open(fullpath + '/.virustotal.key', 'r')
    except: 
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.virustotal.key")

    for line in keyfile:
        vtkey = line.rstrip()
    keyfile.close()
    return vtkey


def check_domain(adomain):
    """Check a domain name against VT"""
    vtkey = load_apikey()
    vturl = "https://www.virustotal.com/vtapi/v2/domain/report"
    parameters = {"domain": adomain, "apikey": vtkey }
    try:
        resp = requests.get(vturl, params=parameters)
    except:
        sys.exit("Problem with the HTTP request to VT")
    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Nothing found for domain: " + adomain) 

    url_list = report.get("detected_urls", {})
    for url in url_list:
        evilness = url['positives']
    
    return evilness


def docheck(adomain):
    """Run checks against the supplied IP address and domain"""
    evildomain = check_domain(adomain)
    if evildomain > 0:
        print adomain + ": [EVIL]"
    else:
        print adomain + ": [OK]"


def __main__():
    """Lets get this party started"""        
    parser = argparse.ArgumentParser(description='Simple virustotal.com domain checker')
    parser.add_argument('--domain', '-d', dest='domain', help='Submit a domain name for checking')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    adomain = args.domain

    if adomain:
        docheck(adomain)
    else:
        sys.exit(parser.print_help())        



if __name__ == "__main__":
        __main__()

