#!/usr/bin/python
# Simple script to expand a bitly link

import requests
import argparse
import json
import sys
import os


def expandurl(url):
    """Check our hash against the Bit.ly API"""
    print "Expanding Bit.ly URL...",
    headers = {'Content-type': 'application/json', "User-Agent": "curl/7.43.0"}
    try:
        token = os.environ['BITLY_TOKEN']
    except Exception as err:
        sys.exit("No API token exported")
    bitlyurl = "https://api-ssl.bitly.com/v3/expand?access_token=" + token + "&hash=" + url + "&format=json"
    try:
        req = requests.get(bitlyurl, headers=headers, verify=True).json()
        print req['status_code']
        if req['status_code'] == 404:
            print "We got a 404."
        elif req['status_code'] == 200:
            print "Expanded URL: " + req['data']['expand'][0]['long_url']
        elif req['status_code'] == 500:
            print "We got a " + req['status_code']
    except Exception as err:
        print "Nope..."


def __main__():
    """Lets get this party started"""
    parser = argparse.ArgumentParser(description='Expand a Bit.ly URL', usage='%(prog)s -u URL')
    parser.add_argument('--url', '-u', dest='url', help='URL to expand')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    url = args.url

    if args.url:
        expandurl(url)
    else:
        print "Exiting"


if __name__ == '__main__':
    __main__()
