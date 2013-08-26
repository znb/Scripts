#!/usr/bin/python
# Simple script to grab the raw output from pastebin
# Yes, you can use wget...but where's the fun in that ?

import sys
import argparse
import httplib


def pastegrabber(arg_file):
    """Grab the pastebin file and dump it locally"""
    host = "pastebin.com"
    connect = httplib.HTTPConnection(host)
    raw_url = "/raw.php?i=" + arg_file
    connect.request("GET", raw_url)
    response = connect.getresponse()
    if response.status != 200:
        sys.exit('Error!', 'status code:', response.status)
    raw_post = response.read()
    write_paste(raw_post)


def write_paste(raw_post):
    """write our pastebin output to file"""
    filename = arg_file + ".txt"
    print "writing to " + filename
    output = open(filename, 'w')
    output.write(raw_post)
    output.close()
    print "We're done here."


def __main__():

    parser = argparse.ArgumentParser(description='basic pastebin grabber', usage='%(prog)s -i ID')
    parser.add_argument('-i', dest='filein', help='pastebin to grab')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    global arg_file
    arg_file = args.filein

    if not args.filein:
        sys.exit(parser.print_help())

    print "Grabbing pastebin id: " + arg_file
    try:
        pastegrabber(arg_file)
    except:
        print "Something went wrong"

if __name__ == '__main__':
    __main__()
