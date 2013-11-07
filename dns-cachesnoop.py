#!/usr/bin/python
# DNS Cache snooping with Scapy

import argparse
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def dnssnoop(adomains, aresolver):
    """Check the server for hosts in our list"""

    domains = open(adomains, 'r')
    for host in domains:
        nhost = host.rstrip('\n')    
        dnsquery = sr1(IP(dst=aresolver)/UDP()/DNS(rd=0,qd=DNSQR(qname=nhost)),verbose=0)
        if "root-servers" in dnsquery[DNSRR].rdata:
            print "Not cached: %s" % nhost
        else:
            print "Cached: " + dnsquery[DNSRR].rrname + "\t\t\tResponse: " + dnsquery[DNSRR].rdata
    domains.close()

def __main__():

    parser = argparse.ArgumentParser(description='dns cache snooping', usage='%(prog)s -d domains.txt')
    parser.add_argument('--domains', '-d', dest='domains', help='file with domains to check')
    parser.add_argument('--resolver', '-r', dest='resolver', help='DNS server to use')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    adomains = args.domains
    aresolver = args.resolver

    if not args.domains and not args.resolver:
        sys.exit(parser.print_help())

    dnssnoop(adomains, aresolver)


if __name__ == '__main__':
    __main__()
