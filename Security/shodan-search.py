#!/usr/bin/python
# Simple Shodan search script

import os
import argparse
import sys
try:
    import shodan
except:
    print "You need the Shodan Python module"
    print "Available here: https://github.com/achillean/shodan-python"
    sys.exit()


def load_apikey():
    """Load API key from file"""
    fullpath = os.getenv("HOME")
    try:
        keyfile = open(fullpath + '/.shodan.key', 'r')
    except:
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.shodan.key")

    for line in keyfile:
        shodankey = line.rstrip()
    keyfile.close()

    return shodankey


def shodan_ip(aip):
    """Search Shodan for our given IP"""
    apikey = load_apikey()
    api = shodan.Shodan(apikey)
    print "Searching..."
    host = api.host(aip)
    print "\nGeneral Information"
    print "-" * 30
    print """
            IP: %s
            Organization: %s
            Operating System: %s
    """ % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a'))

    print "All banner information"
    print "-" * 30
    for item in host['data']:
        print """
                Port: %s
                Banner: %s

        """ % (item['port'], item['data'])


def __main__():
    """Get this party started"""
    print "Shodan API Search"
    parser = argparse.ArgumentParser(description='Simple Shodan Search')
    parser.add_argument('--ip', '-i', dest='ip', help='IP address to search')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aip = args.ip

    if not args.ip:
        sys.exit(parser.print_help())
    else:
        shodan_ip(aip)


if __name__ == '__main__':
    __main__()

