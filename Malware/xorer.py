#!/usr/bin/python

# simple script to XOR encrypt / decrypt text with a key

import argparse
import sys
from itertools import izip, cycle

def main():
	parser = argparse.ArgumentParser(description='xor or unxor text', usage='%(prog)s -i inputfile -k key -o outputfile')
	parser.add_argument('--encrypt', '-e', action='store_true',dest='encrypt', help='encrypt data')
	parser.add_argument('--decrypt', '-d', action='store_true',dest='decrypt', help='decrypt data')
	parser.add_argument('--input', '-i', dest='infile', help='file for input')
	parser.add_argument('--key', '-k', dest='xorkey', help='key to use')
	parser.add_argument('--output', '-o', dest='outfile', help='file for output')
	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	global infile
	global xorkey
	global outfile
	infile = args.infile
	xorkey = args.xorkey
	outfile = args.outfile

	# basic error checking
	if not args.infile:
		parser.print_help()
		sys.exit(1)

	# basic error checking
	if not args.infile:
		parser.print_help()
		sys.exit(1)

	# basic error checking
	if not args.xorkey:
		parser.print_help()
		sys.exit(1)

	# basic error checking
	if not args.outfile:
		parser.print_help()
		sys.exit(1)

	# basic error checking FIX THIS 
	#if not args.encrypt or not args.decrypt:
	#	parser.print_help()
	#	sys.exit(1)

	# do encryption
	if args.encrypt:
		print "encrypting"
		xor_encrypt()

	# do decryption
	if args.decrypt:
		print "decrypting"
		xor_decrypt()


def xor_crypt_string(data, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))

def xor_encrypt():
	global encrypted
	encrypted = open(infile, 'r')
	file_out = open(outfile, 'w')

	print "key: " + xorkey	
	for line in encrypted:
		encrypt_line = xor_crypt_string(line, key=xorkey)
		file_out.write(encrypt_line)
	
	file_out.close()
	encrypted.close()
	print "done."

def xor_decrypt():
	global encrypted
	decrypted = open(infile, 'r')
	file_out = open(outfile, 'w')

	print "key: " + xorkey
	for line in decrypted:
		decrypt_line = xor_crypt_string(line, key=xorkey)
		file_out.write(decrypt_line)
	
	decrypted.close()
	file_out.close()
	print "done."

if __name__ == '__main__':
    main()