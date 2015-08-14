#!/usr/bin/python
# ipinfo.io API requests

import argparse
import sys
import requests


def query_ipinfo(aipaddr):
    """HELP"""
    print "Querying: " + aipaddr
    req = requests.get('http://ipinfo.io/' + str(aipaddr) + '/json')
    if req.status_code == 200:
        print req.text
    else:
        print "Something has gone horribly wrong"


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--ip-addr', '-i', dest='ipaddr', help='IP to query')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aipaddr = args.ipaddr

    if not args.ipaddr:
        sys.exit(parser.print_help())
    else:
        query_ipinfo(aipaddr)


if __name__ == '__main__':
    __main__()
