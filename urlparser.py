#!/usr/bin/python

# simple http parser

import argparse
import sys

def get_urls(filein):
	at = r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))'
   	pat = pat % re.sub(r'([-\\\]])', r'\\\1', string.punctuation)
   	
   	return re.finditer(pat, filein)

def main():

	parser = argparse.ArgumentParser(description='Simple URL parser', usage='%(prog)s -f file')
	parser.add_argument('-f', dest='filein', help='file to parse')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()

	# error checking
	if len(sys.argv)== 1:
		parser.print_help()
		sys.exit(1)

	global filein
	filein = args.filein

	get_urls(filein)

if __name__ == "__main__":
	main()