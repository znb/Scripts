#!/usr/bin/python
# Basic DNS query system

import argparse
import sys
import dns.resolver
import dns.reversename


def rdnsquery(aip):
    """Perform reverse DNS query for IP address"""
    # Not exactly what I'm after
    print dns.reversename.from_address(aip)


def dnsquery(ahost, aqtype):
    """Perform DNS queries"""
    ans = dns.resolver.query(ahost, aqtype)
    if aqtype == "MX":
        for rdata in ans:
            print '>>', rdata.exchange, '\tweight:', rdata.preference
    else:
        try:
            for rdata in ans:
                print rdata.address
        # This isn't working yet :(
        except NoAnswer:
            sys.exit("Error: 31")

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic dns query system', usage='%(prog)s -f file -t <query type>')
    parser.add_argument('--file', '-f', dest='filein', help='file to pull hosts from')
    parser.add_argument('--host', '-H', dest='host', help='Hostname to query')
    parser.add_argument('--ip', '-i', dest='ip', help='IP address to query')
    parser.add_argument('--type', '-t', dest='query', help='DNS query type')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.filein
    aip = args.ip
    ahost = args.host
    aqtype = args.query

    #if not args.filein:
    #    sys.exit(parser.print_help())
    
    if args.host:
        dnsquery(ahost, aqtype)
    elif args.ip:
        rdnsquery(aip)


if __name__ == '__main__':
    __main__()

