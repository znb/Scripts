#!/usr/bin/python
# Simple script to check an email against haveibeenpwned.com

import requests
import argparse
import urllib
import sys

def check_email(aemail):
    """Do the actual checking"""
    print "Checking Email...",
    cemail = urllib.quote(aemail)
    checkurl = "http://haveibeenpwned.com/api/breachedaccount/" + cemail
    r = requests.get(checkurl)
    if r.status_code == 404:
        sys.exit("We're done here.")
    elif r.status_code == 200:
        print "Whoop...bad things happened: ",
        print r.text
        sys.exit("We're done here.")
    else:
        sys.exit("Something else happened")


def __main__():

    parser = argparse.ArgumentParser(description='Check an email against haveibeenpwned.com', usage='%(prog)s -e email')
    parser.add_argument('--email', '-e', dest='email', help='Email to check')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aemail = args.email

    if not args.email:
        sys.exit(parser.print_help())

    check_email(aemail)

if __name__ == '__main__':
    __main__()

