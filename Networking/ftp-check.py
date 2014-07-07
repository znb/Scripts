#!/usr/bin/python
# Simple FTP check script

import argparse
import sys
import ftplib


def check_ftp(rhost):
    """Log into FTP server"""
    print "Checking: " + rhost + " >>",
    ftp = ftplib.FTP(rhost)
    try:
        ftp.login()
    except ftplib.error_perm as e:
        print "something went horribly wrong with logging in."
    print ftp.getwelcome()
    try:
        ftp.retrlines('LIST')
    except ftplib.error_perm as e:
        print "Something went horribly wrong with directory listing."
    ftp.quit()
    print "Done.\n"


def load_file(afile):
    """Load our servers from file"""
    with open(afile, 'r') as fh:
        for line in fh:
            rhost = line.rstrip()
            check_ftp(rhost)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple FTP check script')
    parser.add_argument('--file', '-f', dest='file', help='Pull our FTP server list from this file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file

    if not args.file:
        sys.exit(parser.print_help())
    else:
        load_file(afile)


if __name__ == '__main__':
    __main__()
