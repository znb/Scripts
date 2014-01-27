#!/usr/bin/python
# Simple query tool for statdns.com

import argparse
import sys
import requests


def dnsquery(aqtype, adomain):
    """check statdns.com for our domain"""

    print "Checking domain: " + str(adomain) + " for DNS record type: " + str(aqtype).upper()
    print " >>"
    fullurl = "http://api.statdns.com/" + adomain + "/" + aqtype
    resp = requests.get(fullurl)

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 400:
        print "Error"
    results = report.get("answer", {})
    additional = report.get("additional", {})
    print results
    print additional


def reversequery(adomain):
    """Do a PTR lookup"""
    print "Getting PTR record for: " + str(adomain) 
    fullurl = "http://api.statdns.com/x/" + str(adomain).rstrip('\n')
    resp = requests.get(fullurl)

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 400:
        print "Error"
    results = report.get("answer", {})

    print results

    sys.exit()


def querylist():
    """Print out a list of valid query types"""
    print "Valid query types: ", 
    for query in ['a', 'aaaa', 'cert', 'cname', 'dhcid', 'dlv', 'dname', 'dnskey', 'ds', 
            'hinfo', 'hip', 'ipseckey', 'kx', 'loc', 'mx', 'naptr', 'ns', 'nsec', 
            'nsec3', 'nsec3param', 'opt', 'ptr', 'rrsig', 'soa', 'spf', 'srv', 
            'sshfp', 'tai', 'talink', 'tlsa', 'txt']:
        print query.upper(),

    sys.exit()


def __main__():
    """basic menu system"""
    parser = argparse.ArgumentParser(description='DNS Query tool')
    parser.add_argument('--type', '-t', dest='qtype', help='type of query')
    parser.add_argument('--reverse', '-r', dest='reverse', help='reverse PTR records for query')
    parser.add_argument('--domain', '-d', dest='domain', help='domain/hostname we are interested in')
    parser.add_argument('--list', '-l', dest='querylist', action='store_true', help='list valid query types')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    aqtype = args.qtype
    adomain = args.domain
    areverse = args.reverse

    if args.reverse:
        reversequery(areverse)
    elif args.querylist:
        querylist()
    elif (args.qtype and args.domain):
        dnsquery(aqtype, adomain)
    else:
        sys.exit(parser.print_help())


if __name__ == '__main__':
    __main__()

