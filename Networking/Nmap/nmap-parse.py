#!/usr/bin/python
# basic nmap output parser

import argparse
import sys
try:
    from libnmap.parser import NmapParser
except:
    print "You need the libnmap library"


def report_hosts(nmap_report):
    """Generate a simple report for our scanned hosts"""
    onlinehosts = []
    for host in nmap_report.hosts:
        if host.status == "up":
            onlinehosts.append(host)

    print "Report for scan:"
    for host in onlinehosts:
        print host


def load_scan(afile):
    """Load our scan from file and pull a quick summary"""
    nmap_report = NmapParser.parse_fromfile(afile)
    print "Nmap commandline: " + nmap_report.commandline
    print "Summary: " + nmap_report.summary
    print "Hosts online: " + str(nmap_report.hosts_up)
    report_hosts(nmap_report)

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic nmap output parse')
    parser.add_argument('--file', '-f', dest='file', help='input file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file

    if not args.file:
        sys.exit(parser.print_help())

    load_scan(afile)


if __name__ == '__main__':
    __main__()
