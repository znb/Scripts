#!/usr/bin/python
# FBID Finder
# This is ugly as hell but it'll get the job done

import argparse
import sys
import requests
from bs4 import BeautifulSoup


def search_username(ausername):
    """Search for our usernames numeric ID"""
    print "Searching: " + ausername + " -> ",
    url = "http://www.findmyfbid.com/"
    post_data = "https://www.facebook.com/" + ausername
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0"
    headers = {'User-Agent': user_agent}
    req = requests.post(url, headers=headers, data = { "url": post_data})
    html_data = req.text
    soup = BeautifulSoup(html_data, 'html.parser')
    resp = str(soup.code)
    ugly1 = resp.split(">")
    ugly2 = ugly1[1].split("<")
    if resp == "<code>https://www.facebook.com</code>":
        print "No ID found :("
    else:
        print ugly2[0]

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Facebook ID Finder')
    parser.add_argument('--username', '-u', dest='username', help='Username to search for')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ausername = args.username

    if not args.username:
        sys.exit(parser.print_help())
    else:
        search_username(ausername)


if __name__ == '__main__':
    __main__()
