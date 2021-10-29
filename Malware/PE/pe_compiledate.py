#!/usr/bin/python

# grab the compile time of a piece of malware

import time
import pefile
import sys
import argparse

def parse_pe(arg_file):
	pe = pefile.PE(arg_file)
	epoch = pe.FILE_HEADER.TimeDateStamp
	humantime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch))
	print "Possible compile time: " + humantime 

def __main__():
	parser = argparse.ArgumentParser(description='grab the compile date of a file', usage='%(prog)s -f file')
	parser.add_argument('--file', '-f', dest='filein', help='file to nuke')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	arg_file = args.filein

	if not args.filein:
		sys.exit(parser.print_help())

	try:
		parse_pe(arg_file)
	except:
		print "Error!! Looks like there's a problem with the PE file"
	

if __name__ == '__main__':
    __main__()


