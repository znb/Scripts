#!/usr/bin/python

# shows a summary of ports in use in the pcap

from scapy.all import *
import sys

infile = sys.argv[1]

a = rdpcap(infile)

srcpackets = [ ]

for packet in a:
	srcpackets.append(packet.payload.dport)
		
sorted = sorted(set(srcpackets))

print "port summary for pcap: ", infile

for ip in sorted:
		print ip
		
