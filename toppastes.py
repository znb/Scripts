#!/usr/bin/python
# grab todays top trends from pastebin

import sys
import argparse
from HTMLParser import HTMLParser
from datetime import date
import httplib


class MyHTMLParser(HTMLParser):
    """This will grab the paste ID from the html"""
    def handle_starttag(self, tag, attrs):
        pasteids = []
        for attr in attrs:
            if attr[0] == "href":
                #pasteid = attr[1]
                pasteids.append(attr[1])
                print pasteids
       

def pastegrabber(arg_outdir):
    """Grab todays trending pastes to our specified directory"""
    host = "pastebin.com"
    connect = httplib.HTTPConnection(host)
    trends_url = "/trends"
    connect.request("GET", trends_url)
    response = connect.getresponse()
    if response.status != 200:
        sys.exit('Error!', 'status code:', response.status)
    raw_output = response.read()
    parser = MyHTMLParser()
    ids = parser.feed(raw_output)

    for id in ids:
        print "Paste IDs: " + pasteids[id]


def dump_pastes(arg_outdir):
    """Dump our pastes to the specified directory for later perusal"""
    pastegrabber(arg_outdir)


def __main__():

    parser = argparse.ArgumentParser(description='grab todays trending pastes', usage='%(prog)s -o output')
    parser.add_argument('--outdir', '-o', dest='outdir', help='dump pastes to this directory')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    global arg_outdir
    arg_outdir = args.outdir

    if not args.outdir:
        sys.exit(parser.print_help())

    print "Grabbing top pastes for today "
    print "date: " + str(date.today())
    print "destination " + arg_outdir
    #try:
    #    dump_pastes(arg_outdir)
    dump_pastes(arg_outdir)
    #except:
    #    print "Something went wrong"

if __name__ == '__main__':
    __main__()
