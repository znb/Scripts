#!/usr/bin/python

import argparse
import json
import sys

def menu():
	parser = argparse.ArgumentParser(description='verify json file', usage='%(prog)s -f file')
	parser.add_argument('--file', '-f', dest='filein', help='file to verify')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	args.filein

	if not args.filein:
		sys.exit(parser.print_help())

	try:
		filein = open(args.filein, 'rb')	
		verify = json.loads(filein.read())
		filein.close()
		print "JSON file valid"
	except:
		sys.exit("JSON file invalid")

if __name__ == '__main__':
    menu()

