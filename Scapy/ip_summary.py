#!/usr/bin/python

# gives a summary of the ip addresses used in the pcap

from scapy.all import *
import sys

infile = sys.argv[1]

a = rdpcap(infile)

srcpackets = [ ]

for packet in a:
	srcpackets.append(packet.payload.dst)
		
sorted = sorted(set(srcpackets))

print "ip summary for pcap: ", infile

for ip in sorted:
		print ip
		
