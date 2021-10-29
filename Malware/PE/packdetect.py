#!/usr/bin/python

# simple packer detection script using the PEiD database

import peutils
import pefile
import argparse
import sys

# Adjust this accordingly
USERDB = "/home/matt/tools/UserDB.TXT"


def packdetect(arg_pe):
    """attempt to detect the packer in use"""
    pe = pefile.PE(arg_pe)
    signatures = peutils.SignatureDatabase(USERDB)
    with file(USERDB, 'rt') as f:
        sig_data = f.read()
    signatures = peutils.SignatureDatabase(data = sig_data)
    if arg_showall:
        matches = signatures.match_all(pe, ep_only = True)
    else:
        matches = signatures.match(pe, ep_only = True)
    sys.stdout.write("Possible packer: ")
    print matches


def main():

    # menu system
    parser = argparse.ArgumentParser(description='Basic packer detector', usage='%(prog)s -f file')
    parser.add_argument('--file', '-f', dest='pefile', help='file to check')
    parser.add_argument('--all', '-a', dest='all', help='show all matches', action="store_true")
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    arg_pe = args.pefile
    global arg_showall
    arg_showall = args.all

    if not args.pefile:
        sys.exit(parser.print_help())

    print "analysing..."
    packdetect(arg_pe)


if __name__ == '__main__':
    main()
