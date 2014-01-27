#!/usr/bin/python

import argparse
import sys
import httplib, urllib

def main():

	# menu system
	parser = argparse.ArgumentParser(description='basic menu system', usage='%(prog)s -n nick')
	parser.add_argument('--nick', '-n', dest='nick', help='nick to use')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
	args = parser.parse_args()
	arg_nick = args.nick

	if not args.nick:
		sys.exit(parser.print_help())

	print "ringing on behalf of " + arg_nick
	params = urllib.urlencode({'person': 'buicejox' })
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = httplib.HTTPConnection("door.hackeriet.no")
	conn.request("POST", "", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	print data
	conn.close()

if __name__ == '__main__':
    main()






