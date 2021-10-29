#!/usr/bin/python

# grab the exports of a given dll

import pefile
import sys
import argparse


def parse_dll(arg_dll):

    dll = pefile.PE(arg_dll)
    for exp in dll.DIRECTORY_ENTRY_EXPORT.symbols:
        print hex(dll.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal


def __main__():

    parser = argparse.ArgumentParser(description='check the exports of a given dll', usage='%(prog)s -f file')
    parser.add_argument('--file', '-f', dest='dll', help='dll to examine')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    arg_dll = args.dll

    if not args.dll:
        sys.exit(parser.print_help())

    try:
        parse_dll(arg_dll)
    except:
        print "Error!! Something is wrong...call the police"

if __name__ == '__main__':
    __main__()
