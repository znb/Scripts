#!/usr/bin/python
# Simple DNS test system
# Tests the records in a file against the actual 
# DNS queries for that specific host. 
# Format for input: DNSQUERYTYPE:FQDN:IP
# Example: A:www.zonbi.org:192.168.0.1

import argparse
import sys
import socket
from dns import resolver,reversename, name


def loadfile(afile):
    """Load our file to pull zone info from"""
    print "Resolver: " + adnsserver
    fh = open(afile, 'r')
    for line in fh:
        hostentry = line.rstrip()
        entry = hostentry.split(":", 2)
        lookup = entry[0]
        host = entry[1]
        fip = entry[2]
        if lookup == "PTR":
            print lookup + " record " + host, 
            do_reverse_check(lookup, fip, host)
        else:
            print lookup + " record " + host + " (" + fip + ")", 
            do_check(lookup, fip, host)
    fh.close()


def do_reverse_check(lookup, fip, host):
    """Do PTR record checks"""
    hostfromdns = name.from_text(fip)
    if str(hostfromdns) == str(fip):
        print " [OK] "
    else:
        print " [ERROR!!  DNS:" + str(hostfromdns) + "  FILE: " + fip + "] "


def do_check(lookup, fip, host):
    """Do the actual check of file against DNS"""
    dnsresult = dns_query(adnsserver, lookup, host)    
    if str(dnsresult) == str(fip):
        print " [OK] "
    else:
        print " [ERROR!!  DNS:" + str(dnsresult) + "  FILE: " + fip + "] "


def dns_query(adnsserver, lookup, host):
    """Perform DNS query"""
    dresolver = resolver.Resolver()
    check_dnsserver = adnsserver
    try:
        socket.inet_aton(check_dnsserver)
        cdnsserver = check_dnsserver
    except:
        cdnsserver = socket.gethostbyname(check_dnsserver)

    dresolver.nameservers = [cdnsserver]
    ans = dresolver.query(host, lookup)
    try:
        for rdata in ans:
            return rdata
    except Exception as e:
        print "Error: %s" % e


def __main__():

    parser = argparse.ArgumentParser(description='basic menu system')
    parser.add_argument('--file', '-f', dest='file', default='zones.txt', help='File with DNS entries to check')
    parser.add_argument('--server', '-s', dest='dnsserver', default='8.8.8.8', help='DNS server to query')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    global adnsserver
    adnsserver = args.dnsserver

    if not args.file:
        sys.exit(parser.print_help())

    loadfile(afile)


if __name__ == '__main__':
    __main__()

