#!/usr/bin/python
# Simple bulk hash checker for Virustotal using the requests module
# It expects your VT API Key in ~/.virustotal.key

import argparse
import sys
import os
import requests


def bulkcheck(afile):
    """Bulk checker against VT"""
    vtkey = load_apikey()
    print "Checking hashes in file: " + afile
    try:
        fhandle = open(afile, 'r')
        nlines = sum(1 for line in fhandle)
        if nlines > 4:
            print "*** WARNING: Bulk checks are limited to 4 per minute on the public API ***"
    except IOError, e:
        sys.exit("Error: %s" % e)

    vturl = "https://www.virustotal.com/vtapi/v2/file/report"
    fhandle = open(afile, 'r')
    hashes = fhandle.readlines()
    for hash in hashes:
        try:
            hash = hash.rstrip()
            parameters = {"resource": hash, "apikey": vtkey }
            resp = requests.get(vturl, params=parameters)
            report = resp.json()
            resp_code = report.get("response_code", {})
            if resp_code == 0:
                sys.exit("Exiting. \nGot an unexpected error back from VT")
            evilness = report.get("positives", {})
            totaleng = report.get("total", {})    
            print hash + " Evilness: " + str(evilness) + "/" + str(totaleng)
        except ValueError, e:
            sys.exit("Error: %s" % e)


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

def __main__():

    parser = argparse.ArgumentParser(description='basic menu system', usage='%(prog)s -f file')
    parser.add_argument('--file', '-f', dest='file', help='file with hashes to check')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file

    if not args.file:
        sys.exit(parser.print_help())

    bulkcheck(afile)


if __name__ == '__main__':
    __main__()
