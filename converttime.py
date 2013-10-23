#!/usr/bin/python

# simple time converter which I will probably 
# forget I wrote the next time I need something
# like this. I blame hack.lu

import argparse
import sys
import time

def convert_time(atime):
	"""convert our time to something else"""
	print "time given: " + atime
	epoch = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(atime))
	print epoch

def __main__():

    parser = argparse.ArgumentParser(description='basic time converter', usage='%(prog)s')
    parser.add_argument('--time', '-t', dest='time', help='time to convert')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    atime = args.time

    if not args.time:
        sys.exit(parser.print_help())

    convert_time(atime)


if __name__ == '__main__':
    __main__()