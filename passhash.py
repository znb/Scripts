#!/usr/bin/python

# very simply password hash generator
# because submitting your password to online services is dumb
# code @ zonbi.org

import hashlib,sys
from optparse import OptionParser

def hashgen():

		thisissha1 = hashlib.sha1(mypassword)
		thisismd5 = hashlib.md5(mypassword)

		yoursha1 = thisissha1.hexdigest()
		yourmd5 = thisismd5.hexdigest()

		print "password: ", mypassword
		print "sha1: ", yoursha1
		print "md5: ", yourmd5

def main():
		p = OptionParser(usage="%prog --help", version="%prog 0.1")
		p.add_option("-p",
					type="string",
					dest="password",
					help="password to calculate")
		options, args = p.parse_args()

		if len(args) >= 1:
				print "<<PassHash v0.1>>"
				p.print_help()
				sys.exit()
		else:
				global mypassword
				mypassword = options.password
				hashgen()

if __name__ == "__main__":
		main()
