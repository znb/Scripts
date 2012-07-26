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
	parser.add_argument('-g', action='store_true', dest='graph', help='generate pretty graphs')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	
	# error checking (doesn't seem to work :()
	if len(sys.argv)==0:
		parser.print_help()
		sys.exit(1)

	global arg_file
	global arg_column
	global arg_time
	global arg_graph
	arg_file = args.file
	arg_column = args.column
	arg_time = args.time
	arg_graph = args.graph
	line_num()
	file_parser()

def line_num():
	global num_lines
	num_lines = sum(1 for line in open(arg_file, 'r'))
	
def array_calc():

	print ">> doing magical math stuff"
	print ""
	to9perc = float(to9counter) * 100 / int(num_lines)
	print "io load 0-9% " + str(to9counter) + " times out of " + str(num_lines) + " (" + str(to9perc) + "%)"
	to19perc = float(to9counter) * 100 / int(num_lines)
	print "io load 10-19% " + str(to19counter)  + " times out of " + str(num_lines) + " (" + str(to19perc) + "%)"
	to29perc = float(to9counter) * 100 / int(num_lines)
	print "io load 20-29% " + str(to29counter)  + " times out of " + str(num_lines) + " (" + str(to29perc) + "%)"
	to39perc = float(to9counter) * 100 / int(num_lines)
	print "io load 30-39% " + str(to39counter)  + " times out of " + str(num_lines) + " (" + str(to39perc) + "%)"
	to49perc = float(to9counter) * 100 / int(num_lines)
	print "io load 40-49% " + str(to49counter)  + " times out of " + str(num_lines) + " (" + str(to49perc) + "%)"
	to59perc = float(to9counter) * 100 / int(num_lines)
	print "io load 50-59% " + str(to59counter)  + " times out of " + str(num_lines) + " (" + str(to59perc) + "%)"
	to69perc = float(to9counter) * 100 / int(num_lines)
	print "io load 60-69% " + str(to69counter)  + " times out of " + str(num_lines) + " (" + str(to69perc) + "%)"
	to79perc = float(to9counter) * 100 / int(num_lines)
	print "io load 70-79% " + str(to79counter)  + " times out of " + str(num_lines) + " (" + str(to79perc) + "%)"
	to89perc = float(to9counter) * 100 / int(num_lines)
	print "io load 80-89% " + str(to89counter)  + " times out of " + str(num_lines) + " (" + str(to89perc) + "%)"
	to100perc = float(to9counter) * 100 / int(num_lines)
	print "io load 90-100% " + str(to100counter)+ " times out of " + str(num_lines) + " (" + str(to100perc) + "%)"
	print ""
	if arg_graph:
		print ">> GOTO: GRAPHS"
		print "----------------------------------------------"
		gen_graph()
	else:
		print ">> END"
		print "----------------------------------------------"
		sys.exit(">> thanks for playing.")

def gen_graph():

	print ">> generating graphs"
	# generate graphs here
	print ""
	print ">> END"
	print "----------------------------------------------"
	sys.exit(">> thanks for playing.")


def file_parser():
	print "----------------------------------------------"
	print ">> BEGIN: "
	print "parsing: " + arg_file
	print "lines: " + str(num_lines)
	print "time: " + str(arg_time)
	print "column: " + str(arg_column) 
	print ""
	print ">> GOTO: PARSER"
	print "----------------------------------------------"

	# counters (I'm sure there is a better way to do this)
	global to9counter 
	to9counter = 0
	global to19counter  
	to19counter = 0 
	global to29counter 
	to29counter = 0 
	global to39counter 
	to39counter = 0 
	global to49counter 
	to49counter = 0 
	global to59counter 
	to59counter = 0 
	global to69counter 
	to69counter = 0 
	global to79counter 
	to79counter = 0 
	global to89counter 
	to89counter = 0 
	global to100counter 
	to100counter = 0 

	print ">> parsing entries"
	file_parse = open(arg_file, 'r')
	line_parse = file_parse.readlines()
	for line in line_parse:
		point = int((line.split()[int(arg_column)]))

		if (point >= 0) and (point <= 9):
			# place the value into an array
			#print "1-9: " +  str(point)
			to9counter = to9counter + 1
		elif (point >= 10) and (point <= 19):
			# place the value into an array
			#print "10 - 19: " + str(point)
			to19counter = to19counter + 1
		elif (point >= 20) and (point <= 29):
			# place the value into an array
			#print "20-29: " + str(point)
			to29counter = to29counter + 1
		elif (point >= 30) and (point <= 39):
			# place the value into an array
			#print "30-39: " + str(point)
			to39counter = to39counter + 1
		elif (point >= 40) and (point <= 49):
			# place the value into an array
			#print "40-49: " + str(point)
			to49counter = to49counter + 1
		elif (point >= 50) and (point <= 59):
			# place the value into an array
			#print "50-59: " + str(point)
			to59counter = to59counter + 1
		elif (point >= 50) and (point <= 69):
			# place the value into an array
			#print "60-69: " + str(point)
			to69counter = to69counter + 1
		elif (point >= 70) and (point <= 79):
			# place the value into an array
			#print "70-79: " + str(point)
			to79counter = to79counter + 1			
		elif (point >= 80) and (point <= 89):
			# place the value into an array
			#print "80-89: " + str(point)
			to89counter = to89counter + 1		
		else:
			# place the value into an array
			#print "90-100: " + str(point) 
			to100counter = to100counter + 1	

	print ""
	print ">> GOTO: MATHS"
	print "----------------------------------------------"
	array_calc()
	
if __name__ == '__main__':
    main()