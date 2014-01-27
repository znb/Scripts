#!/usr/bin/python
# Simple query tool for statdns.com

import argparse
import sys
import requests


def dnsquery(aqtype, adomain):
    """check statdns.com for our domain"""

    print "Checking domain: " + str(adomain) + " for DNS record type: " + str(aqtype)
    fullurl = "http://api.statdns.com/" + adomain + "/" + aqtype
    resp = requests.get(fullurl)

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 400:
        print "Error"
    print report

    return 0


def reversequery(adomain):
    """Do a PTR lookup"""
    print "Getting PTR record for: " + str(adomain) 
    fullurl = "http://api.statdns.com/x/" + str(adomain).rstrip('\n')
    print fullurl
    resp = requests.get(fullurl)

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 400:
        print "Error"
    print report

    sys.exit()


def __main__():
    """basic menu system"""
    parser = argparse.ArgumentParser(description='DNS Query tool', usage='%(prog)s -t type -d domain/hostname')
    parser.add_argument('--type', '-t', dest='qtype', help='type of query')
    parser.add_argument('--reverse', '-r', dest='reverse', help='reverse PTR records for query')
    parser.add_argument('--domain', '-d', dest='domain', help='domain/hostname we are interested in')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    aqtype = args.qtype
    adomain = args.domain
    areverse = args.reverse

    if args.reverse:
        reversequery(areverse)
    if not (args.qtype and args.domain):
        sys.exit(parser.print_help())
    else:
        dnsquery(aqtype, adomain)



if __name__ == '__main__':
    __main__()
