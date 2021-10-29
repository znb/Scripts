#!/usr/bin/python
# Spider script to dump all URLs to file

import argparse
import sys
import urllib
import re
from urlparse import urlparse
try:
    from bs4 import BeautifulSoup
    import requests
except:
    print "You're missing libraries"


def spider_url(aurl, afile, aauto, averbose):
    """Spider our given URL and dump links to file"""
    print "\n * Spidering: " + aurl
    au = urlparse(aurl)
    print "\n * Base FQDN: " + au.hostname
    headers = {"User-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    r = requests.get(aurl, headers=headers)
    links = []
    if r.status_code == 200:
        html = r.text
        bs = BeautifulSoup(html)
        for link in bs.find_all('a'):
            links.append((link.get('href')))
    else:
        print "We got something other than a 200"

    # Parse our HTML file and dump links to an list
    print " * Pulling out links..."
    tcount = 0
    urls = []
    for link in links:
        tcount += 1
        if link is None:
            pass
        else:
            if re.match("^https?://", link):
                if link not in urls:
                    urls.append(link)
            elif re.search("#disqus_thread$", link):
                pass
            elif re.match("^/", link):
                full_url = aurl + link
                if full_url not in urls:
                    urls.append(full_url)

    if averbose == 1:
        print "\n * This is our URL list"
        for url in urls:
            print url
    else:
        pass

    print "\n[ Total links: " + str(tcount) + "]"
    if aauto == 1:
        pass
    else:
        raw_input("\nPress ENTER to continue.")
    print "\n * Adding the following URLs for review"

    added = 0
    with open(afile, 'w') as fh:
        for url in urls:
            purl = urlparse(url)
            if purl.hostname != au.hostname:
                pass
            else:
                added += 1
                print url + " ...adding"
                fh.write(url + "\n")
    fh.close()

    print "\n[ Analysis complete...file written. ]"
    print "[ Total links: " + str(tcount) + "]"
    print "[ Added for analysis: " + str(added) + "]"


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Basic site spiderererer')
    parser.add_argument('--url', '-u', dest='url', help='Base URL to start spidering')
    parser.add_argument('--verbose', '-V', dest='verbose', action='store_true', default=False, help='Run with more output')
    parser.add_argument('--auto', '-a', dest='auto', action='store_true', default=True, help='Run as a script')
    parser.add_argument('--file', '-f', dest='file', default='urls.txt', help='File to dump output to')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    aurl = args.url
    aauto = args.auto
    averbose = args.verbose

    if not args.url:
        sys.exit(parser.print_help())
    elif (aauto is False and averbose is False):
        spider_url(aurl, afile, aauto=0, averbose=0)
    elif (aauto and not averbose):
        spider_url(aurl, afile, aauto=1, averbose=0)
    elif (aauto and averbose):
        spider_url(aurl, afile, aauto=1, averbose=1)
    else:
        spider_url(aurl, afile, aauto=1, averbose=0)


if __name__ == '__main__':
    __main__()
