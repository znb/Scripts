#!/usr/bin/python
# Simple redirect checker for URLS

import argparse
import sys
import requests
import re


def parsebody(bodydata):
    """Parsing body for the good stuff"""
    print "\nParsing body"""
    #print bodydata
    


def parseheaders(headerdata):
    """Parsing headers for the good stuff"""
    server = headerdata['server']
    print "`~> Server: " + server

    try:
        location = headerdata['Location']
        if (location) == None:
            parsebody(body)
        else:
            print " `~> Header Redirect: " + location
            print "\n>> New request: " + location + "\n"
            headers = headerrequest(location)
            parseheaders(headers)
    except KeyError:
        print "`~> No location redirects in headers :("


def headerrequest(requrl):
    """Make the HTTP request"""
    req = requests.head(requrl)
    headers = req.headers
    status_code = req.status_code
    history = req.history
    if history == []:
        pass
    else: 
        print "Redirect " + str(history)
    if status_code == 404:
        sys.exit("Erroring out: We got a 404")

    print "Request: " + str(requrl) + "  (" + str(status_code) + ")"

    return headers


def checkurl(url):
    """Check a URL for redirects and the like"""
    headers = headerrequest(url)
    parseheaders(headers)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple redirect follower', usage='%(prog)s -u url')
    parser.add_argument('--url', '-u', dest='url', help='url to check')
    parser.add_argument('--ssl', '-s', dest='ssl', action='store_true', help='URL is SSL enabled')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aurl = args.url
    assl = args.ssl

    if (not args.url and args.ssl):
        sys.exit(parser.print_help())

    regex = re.compile(r'^https?://', re.IGNORECASE)
    sanitycheck = regex.search(aurl)
    if sanitycheck:
        pass
    else:
        if args.ssl:
            aurl = "https://" + aurl
        else:
            aurl = "http://" + aurl
    print "Checking: " + str(aurl) + "\n"
    checkurl(aurl)


if __name__ == '__main__':
    __main__()

