#!/usr/bin/python
# Simple script to expand a short url using the http://longurl.org API

import sys
import argparse
import requests


def urlparse(aurl):
    """Send our URL off for parsing"""
    headers = { "User-Agent" :"shorturl-parser-v1" }
    payload = { 'url' : aurl, 'format' : "json" }
    request = requests.get("http://api.longurl.org/v2/expand?%s", params=payload)
    scode = request.status_code
    if scode == 400:
        sys.exit("We errored out: %s" % scode)
    elif scode == 500:
        print scode, 
        sys.exit("We errored out: %s" % scode)
    elif scode == 400:
        print scode, 
        sys.exit("We errored out: %s" % scode)
    elif scode == 200:
        data = request.json()
        report = data.get("long-url", {})
        print "Expanding: " + aurl + " <~> "+ report


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Short URL expander using longurl.org', usage='%(prog)s -u URL')
    parser.add_argument('--url', '-u', dest='url', help='url to expand')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    aurl = args.url

    if not args.url:
        sys.exit(parser.print_help())
        
    urlparse(aurl)
    
if __name__ == '__main__':
    __main__()
