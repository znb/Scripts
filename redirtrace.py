#!/usr/bin/python
# Simple redirect checker for URLS

import argparse
import sys
import requests


def parsebody(bodydata):
    """Parsing body for the good stuff"""
    print "\nParsing body"""
    #print bodydata
    


def parseheaders(headerdata):
    """Parsing headers for the good stuff"""
    print "Parsing headers"""
    #print headerdata
    server = headerdata['server']
    print "`~> Server: " + server

    try:
        location = headerdata['Location']
        if (location) == None:
            parsebody(body)
        else:
            print " `~> Header Redirect: " + location
            print "\n`~> New request: " + location + "\n"
            headers, body = makerequest(location)
            parseheaders(headers)
    except KeyError:
        print "No location redirects in headers :("


def makerequest(requrl):
    """Make the HTTP request"""
    print "Request: " + str(requrl)
    req = requests.head(requrl)
    headers = req.headers
    bodydata = req.text
    status_code = req.status_code
    history = req.history
    print "Status code: " + str(status_code)
    if history == []:
        pass
    else: 
        print "Redirect " + str(history)
    if status_code == 404:
        sys.exit("Erroring out: We got a 404")

    return (headers, bodydata)


def checkurl(url):
    """Check a URL for redirects and the like"""
    headers, body = makerequest(url)
    parseheaders(headers)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple redirect follower', usage='%(prog)s -u url')
    parser.add_argument('--url', '-u', dest='url', help='url to check')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    global aurl
    aurl = args.url

    if not args.url:
        sys.exit(parser.print_help())

    print "Checking: " + str(aurl) + "\n"
    checkurl(aurl)


if __name__ == '__main__':
    __main__()

