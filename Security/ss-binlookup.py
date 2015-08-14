#!/usr/bin/python
# Shadowserver binary lookup

import argparse
import sys
import json
try:
	import requests
except:
    print "Python requests library required"


def binlookup(ahash):
    """HELP"""
    print "Checking hash against Shadow Server"
    ssurl = "http://bin-test.shadowserver.org/api?md5=" + str(ahash)
    r = requests.get(ssurl)
    if r.status_code == 404:
        print "[ERROR] 404"
    elif r.status_code == 200:
        # There has to be a better way to do this
        raw = r.content.split()
        jdata = raw[1:]
        dump = json.dumps(jdata)
        x = json.loads(dump)
        print "Source: " + x[3].strip(",")
        print "Filename: " + x[5].strip(",")
        print "Product: " + x[9].strip(",")
        print "Manufacturer: " + x[11].strip(",")
        print "Operating System: " + x[14] + x[15]
        print "OS Version: " + x[25].strip(",")
        print "Language: " + x[17].strip(",")
        print "Product Version: " + x[21].strip(",")
        print "File Size: " + x[29].strip(",")
        print "Application: " + x[27].strip(",")
    else:
        print "Something else happened"


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Check executable against a list of known software')
    parser.add_argument('--hash', '-H', dest='hash', help='Hash to lookup')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ahash = args.hash

    if not args.hash:
        sys.exit(parser.print_help())
    else:
        binlookup(ahash)


if __name__ == '__main__':
    __main__()
