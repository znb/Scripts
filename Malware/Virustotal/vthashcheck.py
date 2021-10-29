#!/usr/bin/python
# Simple hash checker for Virus total using the requests module
# It expects your VT API Key in ~/.virustotal.key
# Basic usage ./vthackcheck.py -H <YOURHASH>

import argparse
import sys
import getpass
import requests


def hashcheck(ahash):
    """check hash against the virustotal.com database"""
    vtkey = load_apikey()
    print "Checking hash: " + ahash
    parameters = {"resource": ahash, "apikey": vtkey }
    try:
        resp = requests.get("https://www.virustotal.com/vtapi/v2/file/report", params=parameters)
    except:
        sys.exit()

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Exiting. \nPossibly unknown sample.")
    verb_msg = report.get("verbose_msg", {})
    scan_date = report.get("scan_date", {})
    evilness = report.get("positives", {})
    totaleng = report.get("total", {})
    permalink = report.get("permalink", {})
    scanners = report.get("scans", {})
    print "Message: " + verb_msg
    print "Scan date: " + scan_date
    print "\nMalicious Detects: " + str(evilness) + "/" + str(totaleng)
    print "\nAV detections\n"
    detected = []
    undetected = []
    for scanner in scanners:
        avreport = report.get("scans", {}).get(scanner, {}).get("result")
        avversion = report.get("scans", {}).get(scanner, {}).get("version")
        if avreport == None:
            undetected.append(scanner + " / " + avversion)
        else:
            detected.append(scanner + " / " + avversion + "\t\tDetection: " + str(avreport))

    print "Successful detections: "
    for good in detected:
        print "\t" + good

    print "\nUnsuccessful at detection: "
    for bad in undetected:
        print "\t" + bad

    print "\nPermalink: " + permalink


def load_apikey():
    """Load our API key from file"""
    user = getpass.getuser()
    fullpath = '/home/' + user
    try:
        keyfile = open(fullpath + '/.virustotal.key', 'r')
    except: 
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.virustotal.key")

    for line in keyfile:
        vtkey = line.rstrip()
    keyfile.close()
    return vtkey
    

def __main__():
    """basic menu system"""
    parser = argparse.ArgumentParser(description='virustotal.com hash checker', usage='%(prog)s -H hash')
    parser.add_argument('--hash', '-H', dest='hash', help='hash to check')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    ahash = args.hash

    if not args.hash:
        sys.exit(parser.print_help())

    hashcheck(ahash)


if __name__ == '__main__':
    __main__()
