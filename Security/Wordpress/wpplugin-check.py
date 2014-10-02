#!/usr/bin/python
# Simple script to query the WPScan VulnDB for our plugins

import argparse
import sys
import json
try:
    import requests
except:
    sys.exit("You're missing the Requests library")


def query_api(plugin):
    """Check the API"""
    print "Querying API for " + plugin + " : ",
    url = "https://wpvulndb.com/api/v1/plugins/"
    r = requests.get(url + str(plugin))
    if r.status_code == 404:
        print "No vulnerabilties found.\n"
    else:
        print "Vulnerabilities found."
        jdata = r.json()
        vulns = jdata.get("plugin", {})
        for i in range(len(vulns['vulnerabilities'])):
            vulnerability = vulns['vulnerabilities'][i]['title']
            print "* " + vulnerability
        print "\n"


def parse_json(aplugins):
    """Parse our JSON file"""
    print "Parsing file",
    with open(aplugins, 'r') as json_data:
        data = json.load(json_data)
    json_data.close()
    print "...ok"

    print "Checking plugins for vulnerabilities"
    for i in range(len(data['plugins'])):
        plugin = data['plugins'][i]['title']
        query_api(plugin)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple Vuln checking script')
    parser.add_argument('--plugins', '-p', dest='plugins', help='File with our plugin directory')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aplugins = args.plugins

    if not args.plugins:
        sys.exit(parser.print_help())
    else:
        parse_json(aplugins)


if __name__ == '__main__':
    __main__()

