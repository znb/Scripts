#!/usr/bin/python

# simple time converter which I will probably 
# forget I wrote the next time I need something
# like this. I blame hack.lu

import argparse
import sys
import time

def convert_epoch(aepoch):
	"""convert our time to something else"""
	print "time given: " + aepoch
	epoch = time.strftime("%a %d %b %Y %H:%M:%S +0000", time.gmtime(float(aepoch)))
	print "converted time: " + epoch


def convert_date(adate):
	"""convert regular old dates back to epoch"""
	print "date given: " + adate
	# stuff
	print "epoch time for date: " 

def __main__():

    parser = argparse.ArgumentParser(description='basic time converter', usage='%(prog)s')
    parser.add_argument('--epoch', '-e', dest='epoch', help='convert from epoch')
    parser.add_argument('--date', '-d', dest='date', help='convert from regular old dates')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aepoch = args.epoch
    adate = args.date

    if not args.epoch and not args.date:
        sys.exit(parser.print_help())

    if args.epoch:
    	convert_epoch(aepoch)
    else:
    	convert_date(adate)


if __name__ == '__main__':
    __main__()