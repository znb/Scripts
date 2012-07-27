#!/usr/bin/python

# take iostat output and parse it into something pretty

# -f = file you want to parse
# -c = column you want to investigate
# -s = how many samples you want to parse
# -g = option will create pretty graphs
# -o = option will output to a text file

# Eg. ./iostatparse.py -f c:\iostat.raw -c 21 -s 150 -o c:\iostat_parsed.txt -g c:\iostat_graph.png

# note that this script expects raw iostat output for input. clean it up with: 
# 		cat iostat.txt |  grep -v -e "\(cpu\|id\)" > iostat.raw
# yes, I will add code to clean up files, but in the mean time...

# code@zonbi.org

import argparse
import sys

def main(): # get this party started

	#basic menu system
	parser = argparse.ArgumentParser(description='parse and graph iostat output', usage='%(prog)s -f file -c column -s samples')
	parser.add_argument('-f', dest='file', help='file to parse')
	parser.add_argument('-c', dest='column', help='column to investigate')
	parser.add_argument('-s', dest='samples', help='how many samples to parse')
	parser.add_argument('-o', dest='output', help='write results to file')
	parser.add_argument('-g', action='store_true', dest='graph', help='generate pretty graphs')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	# better way to do this ?
	global arg_file
	global arg_column
	global arg_samples
	global arg_graph
	global arg_output
	arg_file = args.file
	arg_column = args.column
	arg_samples = args.samples
	arg_output = args.output
	arg_graph = args.graph

	line_num()
	file_parser()

def line_num(): # count the number of lines we're parsing
	global num_lines
	num_lines = sum(1 for line in open(arg_file, 'r'))
	
def file_parser(): # parse our file (error checking is for wimps)
	print "----------------------------------------------"
	print ">> BEGIN: "
	print ""
	print "parsing: " + arg_file
	print "max_samples: " + str(num_lines)
	print "samples: " + str(arg_samples)
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
	global to99counter
	to99counter = 0
	global to100counter 
	to100counter = 0 

	print ">> parsing entries"
	max_samples = arg_samples
	file_parse = open(arg_file, 'r')
	for i in range(int(max_samples)):
		line = file_parse.next().strip()
		point = int((line.split()[int(arg_column)]))

		if (point >= 0) and (point <= 9):
			to9counter = to9counter + 1
		elif (point >= 10) and (point <= 19):
			to19counter = to19counter + 1
		elif (point >= 20) and (point <= 29):
			to29counter = to29counter + 1
		elif (point >= 30) and (point <= 39):
			to39counter = to39counter + 1
		elif (point >= 40) and (point <= 49):
			to49counter = to49counter + 1
		elif (point >= 50) and (point <= 59):
			to59counter = to59counter + 1
		elif (point >= 50) and (point <= 69):
			to69counter = to69counter + 1
		elif (point >= 70) and (point <= 79):
			to79counter = to79counter + 1			
		elif (point >= 80) and (point <= 89):
			to89counter = to89counter + 1	
		elif (point >= 90) and (point <= 99):
			to99counter = to99counter + 1	
		else:
			to100counter = to100counter + 1	

	file_parse.close()
	print ""
	print ">> GOTO: MATHS"
	print "----------------------------------------------"
	array_calc()

def array_calc(): # do magic on our counters to get percentages

	print ">> doing magical math stuff"
	print ""

	global to9perc
	to9perc = float(to9counter) * 100 / int(arg_samples)
	print "io load 0-9% " + str(to9counter) + " times out of " + str(arg_samples) + " (" + str(to9perc) + "%)"

	global to19perc
	to19perc = float(to19counter) * 100 / int(arg_samples)
	print "io load 10-19% " + str(to19counter)  + " times out of " + str(arg_samples) + " (" + str(to19perc) + "%)"

	global to29perc
	to29perc = float(to29counter) * 100 / int(arg_samples)
	print "io load 20-29% " + str(to29counter)  + " times out of " + str(arg_samples) + " (" + str(to29perc) + "%)"

	global to39perc
	to39perc = float(to39counter) * 100 / int(arg_samples)
	print "io load 30-39% " + str(to39counter)  + " times out of " + str(arg_samples) + " (" + str(to39perc) + "%)"

	global to49perc
	to49perc = float(to49counter) * 100 / int(arg_samples)
	print "io load 40-49% " + str(to49counter)  + " times out of " + str(arg_samples) + " (" + str(to49perc) + "%)"

	global to59perc
	to59perc = float(to59counter) * 100 / int(arg_samples)
	print "io load 50-59% " + str(to59counter)  + " times out of " + str(arg_samples) + " (" + str(to59perc) + "%)"

	global to69perc
	to69perc = float(to69counter) * 100 / int(arg_samples)
	print "io load 60-69% " + str(to69counter)  + " times out of " + str(arg_samples) + " (" + str(to69perc) + "%)"

	global to79perc
	to79perc = float(to79counter) * 100 / int(arg_samples)
	print "io load 70-79% " + str(to79counter)  + " times out of " + str(arg_samples) + " (" + str(to79perc) + "%)"

	global to89perc
	to89perc = float(to89counter) * 100 / int(arg_samples)
	print "io load 80-89% " + str(to89counter)  + " times out of " + str(arg_samples) + " (" + str(to89perc) + "%)"

	global to99perc
	to99perc = float(to99counter) * 100 / int(arg_samples)
	print "io load 90-99% " + str(to99counter)  + " times out of " + str(arg_samples) + " (" + str(to99perc) + "%)"

	global to100perc
	to100perc = float(to100counter) * 100 / int(arg_samples)
	print "io load 100% " + str(to100counter)+ " times out of " + str(arg_samples) + " (" + str(to100perc) + "%)"

	print ""
	if arg_output:
		print ">> GOTO: OUTPUT"
		print "----------------------------------------------"
		write_output()
	elif arg_graph:
		print ">> GOTO: GRAPHS"
		print "----------------------------------------------"
		gen_graph()
	else:
		print ">> END"
		print "----------------------------------------------"
		sys.exit(">> thanks for playing.")

def write_output(): # write our output to a file if necessary
	print ">> writing results to file"
	print ""
	fileout = open(arg_output, 'a')
	header0 = "\niostatparse 0.1\n"
	header1 = "input file: " + arg_file + "\n"
	header2 = "max samples: " + str(num_lines) + "\n"
	header3 = "samples: " + str(arg_samples) + "\n"
	header4 = "column: " + str(arg_column) + "\n"
	spacer0 = "\n"
	body0 = "io load 0-9% " + str(to9counter) + " times out of " + str(arg_samples) + " (" + str(to9perc) + "%)\n"
	body1 = "io load 10-19% " + str(to19counter)  + " times out of " + str(arg_samples) + " (" + str(to19perc) + "%)\n"
	body2 = "io load 20-29% " + str(to29counter)  + " times out of " + str(arg_samples) + " (" + str(to29perc) + "%)\n"
	body3 = "io load 30-39% " + str(to39counter)  + " times out of " + str(arg_samples) + " (" + str(to39perc) + "%)\n"
	body4 = "io load 40-49% " + str(to49counter)  + " times out of " + str(arg_samples) + " (" + str(to49perc) + "%)\n"
	body5 = "io load 50-59% " + str(to59counter)  + " times out of " + str(arg_samples) + " (" + str(to59perc) + "%)\n"
	body6 = "io load 60-69% " + str(to69counter)  + " times out of " + str(arg_samples) + " (" + str(to69perc) + "%)\n"
	body7 = "io load 70-79% " + str(to79counter)  + " times out of " + str(arg_samples) + " (" + str(to79perc) + "%)\n"
	body8 = "io load 80-89% " + str(to89counter)  + " times out of " + str(arg_samples) + " (" + str(to89perc) + "%)\n"
	body9 = "io load 90-99% " + str(to99counter)+ " times out of " + str(arg_samples) + " (" + str(to99perc) + "%)\n"
	body10 = "io load 100% " + str(to100counter)+ " times out of " + str(arg_samples) + " (" + str(to100perc) + "%)\n"
	footer = "\n<< message ends >>\n"

	fileout.write(header0)
	fileout.write(header1)
	fileout.write(header2)
	fileout.write(header3)
	fileout.write(header4)
	fileout.write(spacer0)
	fileout.write(body0) # I'm pretty sure this can be improved on :D
	fileout.write(body1)
	fileout.write(body2)
	fileout.write(body3)
	fileout.write(body4)
	fileout.write(body5)
	fileout.write(body6)
	fileout.write(body7)
	fileout.write(body8)
	fileout.write(body9)
	fileout.write(body10)
	fileout.write(footer)
	fileout.write(spacer0)
	fileout.close()

	if arg_graph:
		print ">> GOTO: GRAPHS"
		print "----------------------------------------------"
		gen_graph()
	else: 
		print ">> END"
		print "----------------------------------------------"
		sys.exit("<< thanks for playing >>")

def gen_graph(): # create pretty graphs

	print ">> generating graphs"
	# generate graphs here
	print ""
	print ">> END"
	print "----------------------------------------------"
	sys.exit("<< thanks for playing >>")

	

if __name__ == '__main__':
    main()