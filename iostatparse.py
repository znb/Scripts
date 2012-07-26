#!/usr/bin/python

# take iostat output and graph it

import argparse
import sys

def main():

	#basic menu system
	parser = argparse.ArgumentParser(description='parse and graph iostat output', usage='%(prog) -f file -c column')
	parser.add_argument('-f', dest='file', help='file to parse')
	parser.add_argument('-c', dest='column', help='column to parse')
	parser.add_argument('-t', dest='time', help='time slice to parse')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	
	# error checking (doesn't seem to work :()
	if len(sys.argv)==0:
		parser.print_help()
		sys.exit(1)

	global arg_file
	global arg_column
	global arg_time
	arg_file = args.file
	arg_column = args.column
	arg_time = args.time
	line_num()
	file_parser()

def line_num():
	global num_lines
	num_lines = sum(1 for line in open(arg_file, 'r'))
	

def file_parser():
	print "parsing: " + arg_file
	print "lines: " + str(num_lines)
	print "time: " + str(arg_time)
	print "column: " + str(arg_column) 
	print "----------------------------------------------"

	file_parse = open(arg_file, 'r')
	for line in file_parse:
		point = (line.split()[int(arg_column)])
		if point >= 9:
			print "whoop: " +  point
		#elif point >= 10 & =< 19:
		#	print "10 - 19"
		else:
			print "1-9: " + point 


	print "complete"
	#file.close(arg_file)

if __name__ == '__main__':
    main()