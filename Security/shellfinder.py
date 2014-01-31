#!/usr/bin/python 

# Simple PHP shell finder
# Matt Erasmus <code@zonbi.org>

import argparse
import sys

def num_shells():
	global count_shells
	global total_shells

	count_shells = sum(1 for line in open(arg_shellfile, 'r'))
	total_shells = int(count_shells) - 1

def list_shells():
	
	num_shells()
	print "I know about " + str(total_shells) + " shells"
	print "------------------------------------------"
	query = raw_input("Print list ? (y/N): ")
	if query == "y":
		shells = open(arg_shellfile, 'r')
		for line in shells:
			print line	
	else:
		sys.exit("exiting")

	print "<< message ends >>"
	

def main():

	parser = argparse.ArgumentParser(description='find PHP shells on a remote system', usage='%(prog)s -s shellfile -u URL')
	parser.add_argument('--shellfile', '-s', default='shells.dat', dest='shellfile', help='shell file')
	parser.add_argument('--url', '-u', dest='url', help='URL to check')
	parser.add_argument('--recursive', '-r', dest='recursive', help='be recursive in your searches')
	parser.add_argument('--depth', '-d', dest='depth', help='how deep down the rabbit hole')
	parser.add_argument('--list', '-l', action='store_true', dest='list', help='list the shells in our database')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	global arg_shellfile
	global arg_url
	global arg_recursive
	global arg_depth
	global arg_list

	arg_shellfile = args.shellfile
	arg_url = args.url
	arg_recursive = args.recursive
	arg_depth = args.depth
	arg_list = args.list

	if args.list:
		list_shells()


if __name__ == '__main__':
	main()