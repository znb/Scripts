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
    dresolver = dns.resolver.Resolver()
    dresolver.nameservers = [adnsserver]
    ans = dresolver.query(ahost, aqtype)
    if aqtype == "MX":
        try:
            for rdata in ans:
                print '>>', rdata.exchange, '\tweight:', rdata.preference
        except Exception as e:
                print "Error: %s" % e
    else:
        try:
            for rdata in ans:
                print rdata.address
        except Exception as e:
            print "Error: %s" % e

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic dns query system', usage='%(prog)s -f file -t <query type>')
    parser.add_argument('--file', '-f', dest='filein', help='file to pull hosts from')
    parser.add_argument('--host', '-H', dest='host', help='Hostname to query')
    parser.add_argument('--server', '-s', dest='dnsserver', default='8.8.8.8', help='DNS server to query')
    parser.add_argument('--ip', '-i', dest='ip', help='IP address to query')
    parser.add_argument('--type', '-t', dest='query', help='DNS query type')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.filein
    aip = args.ip
    ahost = args.host
    aqtype = args.query
    global adnsserver
    adnsserver = args.dnsserver

    #if not args.filein:
    #    sys.exit(parser.print_help())
    
    if args.host:
        dnsquery(ahost, aqtype)
    elif args.ip:
        rdnsquery(aip)


if __name__ == '__main__':
    __main__()

