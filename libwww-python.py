#!/usr/bin/python
# Simple implementation of libwww-perl in Python 

import argparse
import sys
import requests


def getrequest(aurl, req):
    """Make actual request"""
    if req == "GET":
        resp = requests.get(aurl)
        print ">> GET: " + resp.url
    elif req == "POST":
        resp = requests.get(aurl)
        print ">> POST: " + resp.url
    
    return resp


def headers():
    """Grab HTTP Headers"""
    if aget:
        data = getrequest(aurl, req="GET")
    if apost:
        data = getrequest(aurl, req="POST")
    print " < Status Code: " + str(data.status_code)
    print "\n<< Response"
    print " Headers: " 
    headers = data.headers
    for key, value in headers.items():
        print " < " + key + ": " + value



def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='libwww-perl buti in python', usage='%(prog)s --help')
    parser.add_argument('--url', '-u', dest='url', help='url to do stuff to')
    parser.add_argument('--get', '-G', dest='get', action='store_true', help='GET request')
    parser.add_argument('--post', '-P', dest='post', action='store_true', help='POST request')
    parser.add_argument('--data', '-d', dest='data', help='data for POST request')
    parser.add_argument('--headers', '-H', dest='headers', action='store_true', help='print headers')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    global aurl
    aurl = args.url
    global aget
    aget = args.get
    global apost
    apost = args.post
    adata = args.data
    aheaders = args.headers

    if not args.url:
        sys.exit(parser.print_help())

    if args.headers:
        headers()


if __name__ == '__main__':
    __main__()

