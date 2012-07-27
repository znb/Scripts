#!/usr/bin/python

# take iostat output and parse it into something pretty

# -f = file you want to parse
# -c = column you want to investigate
# -s = how many samples you want to parse
# -g = generate a simple gnuplot file
# -o = option will output to a text file
# -p = clean up a file for parsing

# Eg. ./iostatparse.py -f c:\iostat.raw -c 21 -s 150 -o c:\iostat_parsed.txt -g c:\iostat_graph.png
# NOTE: columns start at 0 in Python so if you want column 15 enter 14...

# code@zonbi.org

import argparse
import sys

def main(): # get this party started

	#basic menu system
	parser = argparse.ArgumentParser(description='parse and graph iostat output', usage='%(prog)s -f file -c column [-s] [-o] [-g] [p]')
	parser.add_argument('--file', '-f', dest='file', help='file to parse')
	parser.add_argument('--column', '-c', dest='column', help='column to investigate')
	parser.add_argument('--samples', '-s', dest='samples', help='how many samples to parse')
	parser.add_argument('--output', '-o', dest='output', help='write results to file')
	parser.add_argument('--gnuplot', '-g', dest='gnuplot', help='generate gnuplot output file')
	parser.add_argument('--prep', '-p', action='store_true', dest='prep', help='prep file for parsing')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	# better way to do this ?
	global arg_file
	global arg_column
	global arg_samples
	global arg_gnuplot
	global arg_output
	arg_file = args.file
	arg_column = args.column
	arg_samples = args.samples
	arg_output = args.output
	arg_gnuplot = args.gnuplot

	# remove all the unneccessary stuff from the file for parsing
	if args.prep:
		file_prep()

	# calculate the number of lines (samples) in the file
	line_num()

	# we need at least the columns to work
	if not args.column:
		parser.print_help()
		sys.exit(1)
	
	# if no sample limit is supplied, parse the whole file
	if not args.samples:
		arg_samples = num_lines
	
	# begin main file parsing
	file_parser()

def file_prep():
	# 		cat iostat.txt |  grep -v -e "\(cpu\|id\)" > iostat.raw
	print "code to clean up file for raw parsing here"

def line_num(): # count the number of lines we're parsing
	global num_lines
	num_lines = sum(1 for line in open(arg_file, 'r'))
	
def file_parser(): # parse our file (error checking is for wimps)
	print "----------------------------------------------"
	print ">> BEGIN "
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
	global to19counter
	global to29counter 
	global to39counter 
	global to49counter 
	global to59counter 
	global to69counter 
	global to79counter 
	global to89counter 
	global to99counter
	global to100counter 

	to9counter = 0
	to19counter = 0 
	to29counter = 0 
	to39counter = 0 
	to49counter = 0 
	to59counter = 0 
	to69counter = 0 
	to79counter = 0 
	to89counter = 0 
	to99counter = 0
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

	# better way to do this ?
	global to9perc
	global to19perc
	global to29perc
	global to39perc
	global to49perc
	global to59perc
	global to69perc
	global to79perc
	global to89perc
	global to99perc
	global to100perc

	# perhaps a loop of some kind here ?
	to9perc = float(to9counter) * 100 / int(arg_samples)
	to19perc = float(to19counter) * 100 / int(arg_samples)
	to29perc = float(to29counter) * 100 / int(arg_samples)
	to39perc = float(to39counter) * 100 / int(arg_samples)
	to49perc = float(to49counter) * 100 / int(arg_samples)
	to59perc = float(to59counter) * 100 / int(arg_samples)
	to69perc = float(to69counter) * 100 / int(arg_samples)
	to79perc = float(to79counter) * 100 / int(arg_samples)
	to89perc = float(to89counter) * 100 / int(arg_samples)
	to99perc = float(to99counter) * 100 / int(arg_samples)
	to100perc = float(to100counter) * 100 / int(arg_samples)

	print ">> GOTO: RESULTS"
	print "----------------------------------------------"
	print ">> results from: " + arg_file
	print ""

	# perhaps a loop of some kind here ?
	print "io load 0-9% " + str(to9counter) + " times out of " + str(arg_samples) + " (" + str(to9perc) + "%)"
	print "io load 10-19% " + str(to19counter)  + " times out of " + str(arg_samples) + " (" + str(to19perc) + "%)"
	print "io load 20-29% " + str(to29counter)  + " times out of " + str(arg_samples) + " (" + str(to29perc) + "%)"
	print "io load 30-39% " + str(to39counter)  + " times out of " + str(arg_samples) + " (" + str(to39perc) + "%)"
	print "io load 40-49% " + str(to49counter)  + " times out of " + str(arg_samples) + " (" + str(to49perc) + "%)"
	print "io load 50-59% " + str(to59counter)  + " times out of " + str(arg_samples) + " (" + str(to59perc) + "%)"
	print "io load 60-69% " + str(to69counter)  + " times out of " + str(arg_samples) + " (" + str(to69perc) + "%)"
	print "io load 70-79% " + str(to79counter)  + " times out of " + str(arg_samples) + " (" + str(to79perc) + "%)"
	print "io load 80-89% " + str(to89counter)  + " times out of " + str(arg_samples) + " (" + str(to89perc) + "%)"
	print "io load 90-99% " + str(to99counter)  + " times out of " + str(arg_samples) + " (" + str(to99perc) + "%)"
	print "io load 100% " + str(to100counter)+ " times out of " + str(arg_samples) + " (" + str(to100perc) + "%)"

	print ""
	if arg_output:
		print ">> GOTO: OUTPUT"
		print "----------------------------------------------"
		write_output()
	elif arg_gnuplot:
		print ">> GOTO: GNUPLOT"
		print "----------------------------------------------"
		gen_gnuplot()
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

	# perhaps a loop of some kind here ?
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

	if arg_gnuplot:
		print ">> GOTO: GNUPLOT"
		print "----------------------------------------------"
		gen_gnuplot()
	else: 
		print ">> END"
		print "----------------------------------------------"
		sys.exit("<< thanks for playing >>")

def gen_gnuplot(): # create a gnuplot file

	print ">> generating gnuplot file"
	# generate graphs heres
	#
	print ">> writing plot file" # write the plot file for gnuplot to use
	arg_gnuplot_plot = arg_gnuplot + ".plt"
	fileout = open(arg_gnuplot_plot, 'w')
	body0 = "set terminal png size 1280,600\n"
	body1 = "set output \"" + arg_gnuplot + ".png\"\n"
	body2 = "set title \"IO load\"\n"
	body3 = "set yrange[0:100]\n"
	body4 = "set boxwidth 0.5\n"
	body5 = "set style fill solid\n"
	body6 = "plot \"" + arg_gnuplot + ".raw\" using 1:3:xtic(2) with boxes title 'io load'\n"
	# perhaps a loop of some kind here ?
	fileout.write(body0)
	fileout.write(body1)
	fileout.write(body2)
	fileout.write(body3)
	fileout.write(body4)
	fileout.write(body5)
	fileout.write(body6)
	fileout.close()

	print ">> writing data file"  # write the raw gnuplot file to plot from
	print ""
	arg_gnuplot_raw = arg_gnuplot + ".raw"
	fileout = open(arg_gnuplot_raw, 'w')
	body0 = "0 0-9% " + str(to9perc) + "\n" 
	body1 = "1 10-19% " + str(to19perc) + "\n" 
	body2 = "2 20-29% " + str(to29perc) + "\n" 
	body3 = "3 30-39% " + str(to39perc) + "\n" 
	body4 = "4 40-49% " + str(to49perc) + "\n" 
	body5 = "5 50-59% " + str(to59perc) + "\n" 
	body6 = "6 60-69% " + str(to69perc) + "\n" 
	body7 = "7 70-79% " + str(to79perc) + "\n" 
	body8 = "8 80-89% " + str(to89perc) + "\n" 
	body9 = "9 90-99% " + str(to99perc) + "\n" 
	body10 = "10 100% " + str(to100perc) + "\n" 
	# perhaps a loop of some kind here ?
	fileout.write(body0)
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
	fileout.close()

	print ""
	print "file output: " + arg_gnuplot
	print ""

 	print ">> END"
	print "----------------------------------------------"
	sys.exit("<< thanks for playing >>")

	

if __name__ == '__main__':
    main()