#!/usr/bin/python
# Simple base64 decoder 

import sys
import argparse

def b64decode(adecode):
	"""Decode base64 stuff given to us"""
	print "Decoding: " + adecode
	try:
		print adecode.decode("base64")
	except Exception, err:
		sys.exit("Error: %s" % str(err))		

def b64encode(aencode):
	"""Encode stuff given to us into base64"""
	print "Encoding: " + aencode
	try:
		print aencode.encode("base64")
	except Exception, err:
		sys.exit("Error: %s" % str(err))

def __main__():

    parser = argparse.ArgumentParser(description='basic base64 {en,de}coder', usage='%(prog)s -e stuff / -d stuff')
    parser.add_argument('--decode', '-d', dest='decode', help='stuff to decode')
    parser.add_argument('--encode', '-e', dest='encode', help='stuff to encode')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    adecode = args.decode
    aencode = args.encode
    
    if args.decode:
    	b64decode(adecode)
    elif args.encode:
    	b64encode(aencode)
    else:
    	sys.exit(parser.print_help())


if __name__ == '__main__':
    __main__()
