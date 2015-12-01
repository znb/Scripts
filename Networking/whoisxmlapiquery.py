#!/usr/bin/python
# Whois query from https://www.whoisxmlapi.com

import sys
import json
import requests
import argparse


def query_api(QUERY, OUTPUT):
    """HELP"""
    print "Query: " + str(QUERY)
    full_query = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=' + QUERY + '&outputFormat=json'
    req = requests.get(full_query)
    if req.status_code == 200:
        jdata = req.json()
        print jdata
        print "Dumping JSON report"
        with open(OUTPUT, 'w') as fh:
            json.dump(jdata, fh)
    else:
        print "[ERROR] Code: " + req.status_code


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='DESCRIPTION HERE')
    parser.add_argument('--query', '-q', dest='query', help='Domain/IP to query')
    parser.add_argument('--output', '-o', dest='output', default='whois.json', help='Output file to write')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    QUERY = args.query
    OUTPUT = args.output

    if not args.query:
        sys.exit(parser.print_help())
    else:
        query_api(QUERY, OUTPUT)


if __name__ == '__main__':
    __main__()
