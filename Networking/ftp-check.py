#!/usr/bin/python
# Simple FTP check script

import argparse
import sys
import ftplib
import errno
import socket


def check_ftp(rhost):
    """Log into FTP server"""
    try:
        ftp = ftplib.FTP(rhost, timeout=10)
    except socket.error as e:
        print "Problem connecting...moving on"
        problem_hosts.append(rhost)
    else:
        try:
            ftp.login()
        except ftplib.error_perm as e:
            print "something went horribly wrong with logging in."
            problem_hosts.append(rhost)
        print ftp.getwelcome()
        try:
            ftp.retrlines('LIST')
        except ftplib.error_perm as e:
            print "Something went horribly wrong with directory listing."
            problem_hosts.append(rhost)
        ftp.quit()
        print "Done.\n"

    return problem_hosts


def load_file(afile):
    """Load our servers from file"""
    with open(afile, 'r') as fh:
        global problem_hosts
        problem_hosts = []
        for line in fh:
            rhost = line.rstrip()
            print "Checking: " + rhost + " >>",
            checks = check_ftp(rhost)

    print "[*] Scanning complete"
    print "\n[*] Problems with the following hosts: "
    for host in checks:
        print "\t" + host


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
