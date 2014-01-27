#!/usr/bin/python
# Simple rotX decoder

import argparse
import string
import sys


def derot(astring):
    """Do some bit shifting"""
    rot13 = string.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    output = string.translate(astring, rot13)
    print output


def menu():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic menu system', usage='%(prog)s -r rotation')
    parser.add_argument('--string', '-s', dest='string', help='string to tinker with')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    astring = args.string

    if not args.string:
        sys.exit(parser.print_help())

    derot(astring)

if __name__ == '__main__':
    menu()
