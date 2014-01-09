#!/usr/bin/python
# Simple redirect checker for URLS

import argparse
import sys
import requests

def checkurl(aurl):
    """Check a URL for redirects and the like"""
    print "Checking: " + aurl
    req = requests.get(aurl, allow_redirects=False)
    sc = req.status_code
    if sc == 404:
        sys.exit("We got a 404")


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple redirect follower', usage='%(prog)s -u url')
    parser.add_argument('--url', '-u', dest='url', help='url to check')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aurl = args.url

    if not args.url:
        sys.exit(parser.print_help())

    checkurl(aurl)


if __name__ == '__main__':
    __main__()

