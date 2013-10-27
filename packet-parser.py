#!/usr/bin/python

# Pull out all the arguements from an HTTP Post 
# For this challenge: http://blog.handlerdiaries.com/?p=63

import argparse
import sys
import os
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def pullpackets(apackets):
    """file handler"""
    print "[*] Parsing packet capture"
    tmpfile = "/tmp/outtmp.txt"
    f = open(tmpfile, 'w')
    packets = rdpcap(apackets)
    a = ''
    for payload in packets:
        a += payload.load + "\n\n"
    f.write(a)
    f.close()
    pullcmd(tmpfile)

def pullcmd(tmpfile):
    """pull commands from the packet payloads"""
    print "[*] Pulling out commands"
    p = open(tmpfile, 'r')
    o = open(aoutput, 'w')
    for line in p:
        if 'cmd' in line and not 'http' in line:   # we want the cmd's but not the Referer lines
            o.write(line)
    p.close()
    os.remove(tmpfile)   # clean up temp file
    o.close()
    print "[*] Output: " + aoutput

def __main__():
    """Main"""
    parser = argparse.ArgumentParser(description='basic menu system', usage='%(prog)s -p pcapfile')
    parser.add_argument('--packets', '-p', dest='packets', help='packet capture to parse')
    parser.add_argument('--output', '-o', dest='output', help='output file', default='output.txt')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    apackets = args.packets
    global aoutput
    aoutput = args.output

    if not apackets:
        sys.exit(parser.print_help())

    pullpackets(apackets)


if __name__ == '__main__':
    __main__()
