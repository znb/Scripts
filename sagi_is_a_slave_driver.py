#!/usr/bin/python

# version 0.2
# TODO
# pass params to functions 

from datetime import date 
import sys
import argparse
import json


def list_birthdays():
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	print "\nBirthdays in file: "
	print "-------------------"
	for x in output_json["birthdays"]:
	   		print x["date"], x["name"]

	sys.exit("\nWe're done here")
	

def search_person():
	print "\nSearching for " + arg_person + "\n"
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	for x in output_json["birthdays"]:
		if x["name"] == arg_person:
			print x["name"] + " has a birthday on: " + x["date"]
		else:
			continue
	
def set_reminder():
	print "super leet reminder code here..."

def check_birthdays():
	print "\nWe're checking if today is special for someone..."
	today = date.today()
	print "\nToday is " + str(today) + "\n"
	output_file = open(arg_file).read()
	output_json = json.loads(output_file)
	for x in output_json["birthdays"]:
		if x["date"] == str(today):
			print x["name"] + " has a birthday today !!"
			reminder = raw_input("Set a reminder Y/N ?")
			if reminder == "y":
				set_reminder()
			else:
				continue
		else:
			continue

def __main__():

	# menu system
	parser = argparse.ArgumentParser(description='basic birthday reminder system', usage='%(prog)s -f file')
	parser.add_argument('--file', '-f', dest='file', help='file with birthdays')
	parser.add_argument('--person', '-p', dest='person', help='person to search for')
	parser.add_argument('--check', '-c', dest='check', action="store_true", help='check if today is a birthday')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()

	# not sure about globals yet 
	global arg_file
	arg_file = args.file
	global arg_person
	arg_person = args.person
	global arg_check
	arg_check = args.check

	if len(sys.argv) <= 1:
		sys.exit(parser.print_help())

	if args.person and arg_file:
		search_person()
	elif arg_file and arg_check:
		check_birthdays()
	else:
		list_birthdays()

if __name__ == '__main__':
    __main__()