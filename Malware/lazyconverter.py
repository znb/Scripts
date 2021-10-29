#!/usr/bin/python

# Simple ascii to hex / hex to ascii converter

# code @ zonbi dot org

import binascii
import sys
import argparse

class Converter(object):
	"""Convert stuff"""

	def convert_to_ascii(self):
		print "converting hex to ascii"
		print "hex: " + con_string
		#output = binascii.hexlify(con_string)
		output = con_string.decode("hex")
		print "ascii: " 

	def convert_to_hex(self):
		print "converting ascii to hex"
		print "ascii: " + con_string 
		output = con_string.encode("hex")
		print "hex: " + output

def main():
	parser = argparse.ArgumentParser(description='basic converter', usage='%(prog)s -x/-a -s INPUT')
	parser.add_argument('--ascii', '-a', dest='ascii', action='store_true', help='convert to ascii')
	parser.add_argument('--hex', '-x', dest='hex', action='store_true', help='convert to hex')
	parser.add_argument('--string', '-s', dest='constring', help='string to convert')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		sys.exit(parser.print_help())

	global arg_ascii
	global arg_hex
	global con_string
	arg_ascii = args.ascii
	arg_hex = args.hex
	con_string = args.constring

	if args.ascii:
		con = Converter()
		con.convert_to_ascii()	
	elif args.hex:
		con = Converter()
		con.convert_to_hex()
	else:
		sys.exit(parser.print_help())



if __name__ == '__main__':
    main()