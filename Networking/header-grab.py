#!/usr/bin/python
# Simple script to grab the headers from a bunch of hosts

import argparse
import sys
import requests


def list_headers():
    """Dump a list of known headers"""
    print "Some common headers to check for\n"
    headers = ['Accept', 'Accept-Encoding', 'Authorization', 'Cache-Control', 'Cookie', 'Content-Type',
               'Host', 'User-agent', 'Via', 'Server', 'P3P', 'Status']

    for header in headers:
        print header
    sys.exit("\nWe're done here")


def pull_headers(ahost, aheader):
    """Pull the headers from our host URL"""
    print "Checking: " + ahost + " -> ",
    try:
        req = requests.get(ahost, verify=False, timeout=60)
    except Exception, err:
        print "Something has gone horribly wrong: %s" % err

    if req.status_code == 200:
        print req.headers[aheader]
    else:
        print "Status code: " + str(req.status_code)


def parse_file(ainfile, aheader):
    """Parse our input file"""
    try:
        print "Parsing input file"
        with open(ainfile, 'r') as fh:
            for host in fh:
                pull_headers(str(host.strip()), aheader)
    except Exception, err:
        sys.exit("[ERROR] Something has gone horribly wrong: %s" % err)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='HTTP Header Grabber')
    parser.add_argument('--infile', '-f', dest='infile', help='Input file of hosts')
    parser.add_argument('--header', '-H', dest='header', default='server', help='Header to check')
    parser.add_argument('--supported-headers', '-l', dest='listing', action='store_true', help='List common headers')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ainfile = args.infile
    aheader = args.header
    alisting = args.listing

    if args.listing:
        list_headers()

    if not args.infile:
        sys.exit(parser.print_help())
    else:
        parse_file(ainfile, aheader)


if __name__ == '__main__':
    __main__()

