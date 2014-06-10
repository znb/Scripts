#!/usr/bin/python
# Wifi Summary from Kismet

import argparse
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import pprint


def load_file(afile, aoutput):
    """Load our packet capture"""
    print "Parsing Kismet output"
    pkts = rdpcap(afile)
    bssid_list = {}
    for packet in pkts:
        if packet.haslayer(Dot11Beacon):
            bssid = packet.sprintf("%Dot11Elt.info%")
            ssid = packet.sprintf("%Dot11.addr2%")
            if bssid in bssid_list:
                bssid_list[bssid].add(ssid)
            else:
                bssid_list[bssid] = {ssid}
        else:
            pass
    # Make this prettier
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(bssid_list)

    print "\nWe're done here"


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Simple Wifi Beacon Summary Script')
    parser.add_argument('--file', '-f', dest='file', help='Packet dump file')
    parser.add_argument('--output', '-o', dest='output', default='wifi-networks.txt', help='Output file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    aoutput = args.output

    if not args.file:
        sys.exit(parser.print_help())
    else:
        load_file(afile, aoutput)


if __name__ == '__main__':
    __main__()

