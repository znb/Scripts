#!/usr/bin/python

# Simple python listener
# Bugs ? code@zonbi.org

import socket, sys

if len(sys.argv) < 4:
		sys.exit("Usage: " + sys.argv[0] + " <proto> <port> <output>")

lproto = sys.argv[1]
lport = int(sys.argv[2])
outfile = sys.argv[3]

print "Firing up "+ lproto + " listener on ", lport
print "Writing to file", outfile
print "-------------------------------------"

if lproto == "tcp":
	proto = socket.SOCK_STREAM
elif lproto == "udp":
	proto = socket.SOCK_DGRAM
else:	
	sys.exit("Wrong protocol.")

socket = socket.socket(socket.AF_INET,proto)
socket.bind(('', lport))
socket.listen(5)

while 1:
	connection, addr = socket.accept()
	print "New connection from: ", addr
	data = connection.recv(1024)
	connection.close()
	print "Data received: ", data
	outputfile = open(outfile, "a")
	outputfile.write(data)
	
socket.close()
outputfile.close()
