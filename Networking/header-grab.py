#!/usr/bin/python
# Simple script to grab the headers from a bunch of hosts

import argparse
import sys
import requests


def pull_headers(ahost):
    """Pull the headers from our host URL"""
    print "Checking: " + ahost + " -> ",
    try:
        req = requests.get(ahost, verify=False, timeout=60)
    except Exception, err:
        print "Something has gone horribly wrong: %s" % err

    if req.status_code == 200:
        print req.headers['server']
    else:
        print "Status code: " + str(req.status_code)


def parse_file(ainfile):
    """Parse our input file"""
    try:
        print "Parsing input file"
        with open(ainfile, 'r') as fh:
            for host in fh:
                pull_headers(str(host.strip()))
    except:
        sys.exit("[ERROR] Unable to open input file")


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Hi Mom')
    parser.add_argument('--infile', '-f', dest='infile', help='Input file of hosts')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ainfile = args.infile

    if not args.infile:
        sys.exit(parser.print_help())
    else:
        parse_file(ainfile)


if __name__ == '__main__':
    __main__()

