#!/usr/bin/python
# Simple script to check an email against haveibeenpwned.com

import requests
import argparse
import urllib
import sys


def do_check(checkemail):
    """Do the actual checking against HIBP"""
    checkurl = "http://haveibeenpwned.com/api/breachedaccount/" + urllib.quote(checkemail)
    r = requests.get(checkurl)
    if r.status_code == 404:
        print "You're good, " + checkemail + " not found."
    elif r.status_code == 200:
        print "Bad things happened: " + checkemail + " found on lists",  
        print r.text
    else:
        print "Something else happened"


def check_email(aemail):
    """Do the actual checking"""
    print "Checking Email...",
    do_check(aemail)


def check_email_list(aelist):
    """Check a list of emails against HIBP"""
    print "Checking email list: " + aelist
    f = open(aelist, 'r')
    for email in f:
        do_check(email.rstrip())
    f.close()

def __main__():
    """Lets get this party started"""
    parser = argparse.ArgumentParser(description='Check an email against haveibeenpwned.com', usage='%(prog)s -e email')
    parser.add_argument('--email', '-e', dest='email', help='Email to check')
    parser.add_argument('--list', '-l', dest='email_list', help='Email list to check, one email per line')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2')
    args = parser.parse_args()
    aemail = args.email
    aemail_list = args.email_list

    if not (args.email or args.email_list):
        sys.exit(parser.print_help())

    if args.email_list:
        check_email_list(aemail_list)
    else:
        check_email(aemail)

if __name__ == '__main__':
    __main__()

