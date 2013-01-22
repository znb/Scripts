#!/usr/bin/python

from datetime import date 
import sys
import argparse
import json


def list_birthdays():
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	for i in output_json:
	    print "\nBirthdays in file: "
	    print "-------------------"
    	for k in output_json[i]:
            print k, output_json[i][k]
    
	sys.exit("\nWe're done here")
	

def search_person():
	print "\nSearching for " + arg_person
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	print "Birthday on: " + output_json['birthdays'][arg_person]
	sys.exit("We're done here")


def check_birthdays():
	print "\nWe're checking if today is special for someone..."
	today = date.today()
	print "\nToday is " + str(today)
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	for i in output_json:
		search_date = output_json["birthdays"]["date"]
		if str(search_date) == str(today):
			print "It's " + output_json["birthdays"]["person"] + "\'s birthday today."
		else:
			print "\nNo birthdays today."
	

def menu():

	# menu system
	parser = argparse.ArgumentParser(description='basic birthday reminder system', usage='%(prog)s -f file')
	parser.add_argument('--file', '-f', dest='file', help='file with birthdays')
	parser.add_argument('--person', '-p', dest='person', help='person to search for')
	parser.add_argument('--check', '-c', dest='check', action="store_true", help='check if today is a birthday')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()

	if len(sys.argv) == 1:
		sys.exit(parser.print_help())

	# not sure about globals yet 
	global arg_file
	arg_file = args.file
	global arg_person
	arg_person = args.person
	global arg_check
	arg_check = args.check

	if not args.file:
		sys.exit(parser.print_help())

	if args.person and arg_file:
		try:
			search_person()	
		except:
			print "Person not in database :("
	elif arg_file and arg_check:
		check_birthdays()
		#try:
		#	check_birthdays()
		#except:
		#	print "Today isn't a special day :("
	else:
		list_birthdays()
	


if __name__ == '__main__':
    print "\nDo your homework or Sagi will punish you !!\n"
    menu()