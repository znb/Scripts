#!/usr/bin/python
# Simple GeoIP DB lookup

import argparse
import sys
import os
import geoip2.database

def checkip():
    """Check the IP address against our DB"""
    print "Checking IP's"


def checkdb():
    """Check that our DB files exist"""
    print "Checking databases"

    fullpath = os.getenv("HOME")
    try:
        dbfile = open(fullpath + '/.glcountry.mmdb', 'r')
    except: 
        sys.exit("** ERROR ** \n> Database file not found. Please check ~/.glcountry.mmdb")

    reader = geoip2.database.Reader(dbfile)
    response = reader.city('128.101.101.101')
    isocode = response.country.iso_code	
    countryname = response.country.name
    cityname = response.city.name

    print "isocode " + isocode
    print "countryname " + countryname
    print "city " + cityname

    #checkip()


def __main__():

    parser = argparse.ArgumentParser(description='basic GeoIP  system', usage='%(prog)s -i IP address')
    parser.add_argument('--ip', '-i', dest='ip', help='IP address to lookup')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aip = args.ip

    if not args.ip:
        sys.exit(parser.print_help())

    checkdb()


if __name__ == '__main__':
    __main__()
