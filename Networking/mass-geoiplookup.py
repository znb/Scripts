#!/usr/bin/python
# Mass geoip lookups

import argparse
import sys
import os
import geoip2.database


def geoip_lookup(ipaddr):
    """Perform GeoIP lookups"""
    homepath = os.getenv("HOME")
    try:
        rd = geoip2.database.Reader(homepath + '/.GeoLite2-Country.mmdb')
    except:
        print "Unable to load Maxmind database"
    try:
        resp = rd.city(ipaddr)
        country = resp.country.name
    except:
        print ipaddr + " not in database"
        country = True

    return country


def load_file(afile):
    """Load our file"""
    with open(afile, 'r') as fh:
        for line in fh:
            ipaddr = line.rstrip()
            country = geoip_lookup(ipaddr)
            print ipaddr + " " + str(country)
    fh.close()


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Mass GeoIP lookups')
    parser.add_argument('--file', '-f', dest='file', help='Pull IP addresses from this file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file

    if not args.file:
        sys.exit(parser.print_help())
    else:
        load_file(afile)


if __name__ == '__main__':
    __main__()
