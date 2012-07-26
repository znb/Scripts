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
	
def array_calc():

	print "parsing complete"
	print "doing magical math stuff"
	gen_graph()

def gen_graph():

	print "generating graphs"
	# generate graphs here
	print "all done"
	sys.exit("thanks for playing")


def file_parser():
	print "parsing: " + arg_file
	print "lines: " + str(num_lines)
	print "time: " + str(arg_time)
	print "column: " + str(arg_column) 
	print "----------------------------------------------"

	file_parse = open(arg_file, 'r')
	line_parse = file_parse.readlines()

	for line in line_parse:
		point = int((line.split()[int(arg_column)]))

		if (point >= 0) or (point <= 9):
			# place the value into an array
			print "1-9: " +  str(point)
		elif (point >= 10) or (point <= 19):
			# place the value into an array
			print "10 - 19: " + str(point)
		elif (point >= 20) or (point <= 29):
			# place the value into an array
			print "20-29" + str(point)
		elif (point >= 30) or (point <= 39):
			# place the value into an array
			print "30-39" + str(point)
		elif (point >= 40) or (point <= 49):
			# place the value into an array
			print "40-49" + str(point)
		elif (point >= 50) or (point <= 59):
			# place the value into an array
			print "50-59" + str(point)
		elif (point >= 50) or (point <= 69):
			# place the value into an array
			print "60-69" + str(point)
		elif (point >= 70) or (point <= 79):
			# place the value into an array
			print "70-79" + str(point)			
		elif (point >= 80) or (point <= 89):
			# place the value into an array
			print "80-89" + str(point)		
		else:
			# place the value into an array
			print "90-100: " + str(point) 

	print "complete"
	array_calc()
	
if __name__ == '__main__':
    main()