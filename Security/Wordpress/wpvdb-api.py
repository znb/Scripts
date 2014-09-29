#!/usr/bin/python
# Simple script to query the WPScan Vulnerability Database API

import argparse
import sys
try:
    import requests
except:
    sys.exit("Python Requests library required")


def query_api(url, check):
    """Check the API"""
    print "Checking API...",
    r = requests.get(url + str(check))
    if r.status_code == 404:
        sys.exit("No vulnerabilties found.")
    if r.status_code != 200:
        sys.exit("Something has gone horribly wrong. Error code: " + str(r.status_code))
    else:
        data = r.json()

    print " ok"
    return data


def wp_theme_check(athemecheck):
    """Checks for vulnerable themes"""
    PLUGIN_API_URL = "https://wpvulndb.com/api/v1/themes/"
    plugin_check = query_api(PLUGIN_API_URL, athemecheck)
    print "Vulnerabilty report"
    vulns = plugin_check.get("theme", {})
    for i in range(len(vulns['vulnerabilities'])):
        vulnerability = vulns['vulnerabilities'][i]['title']
        print vulnerability


def wp_plugin_check(aplugincheck):
    """Checks for vulnerable plugins"""
    PLUGIN_API_URL = "https://wpvulndb.com/api/v1/plugins/"
    plugin_check = query_api(PLUGIN_API_URL, aplugincheck)
    print "Vulnerabilty report"
    vulns = plugin_check.get("plugin", {})
    for i in range(len(vulns['vulnerabilities'])):
        vulnerability = vulns['vulnerabilities'][i]['title']
        print vulnerability


def wp_version_check(awpcheck):
    """Checks for vulnerable Wordpress version"""
    WP_API_URL = "https://wpvulndb.com/api/v1/wordpresses/"
    wp_check = query_api(WP_API_URL, awpcheck)
    print "Vulnerabilty report"
    vulns = wp_check.get("wordpress", {})
    for i in range(len(vulns['vulnerabilities'])):
        vulnerability = vulns['vulnerabilities'][i]['title']
        print vulnerability


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='WPScan Vulnerability Database API Search Tool of Doom')
    parser.add_argument('--wordpress', '-w', dest='wpcheck', help='Is my Wordpress vulnerable')
    parser.add_argument('--themes', '-t', dest='themecheck', help='Is my Wordpress theme vulnerable')
    parser.add_argument('--plugin', '-p', dest='plugincheck', help='Is my Wordpress plugin vulnerable')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    global awpcheck
    awpcheck = args.wpcheck
    global athemecheck
    athemecheck = args.themecheck
    global aplugincheck
    aplugincheck = args.plugincheck

    if args.wpcheck:
        wp_version_check(awpcheck)
    elif args.themecheck:
        wp_theme_check(athemecheck)
    elif args.plugincheck:
        wp_plugin_check(aplugincheck)
    else:
        sys.exit(parser.print_help())


if __name__ == '__main__':
    __main__()
