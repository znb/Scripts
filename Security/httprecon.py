#!/usr/bin/python
# simple script to pull common web stuff for recon purposes
# Matt Erasmus code@zonbi.org

import httplib
import sys

sys.argv.pop(0)
if len(sys.argv) == 0:
	print "please give us a test host"
	sys.exit(1)
	
host = sys.argv[0]

print ""
print "		<< HTTPRecon Script >> 	"
print "<----------------------------------------------->"
print ""

# Headers
print "Headers for ", host
print "<----------------------------------------------->"
connect = httplib.HTTPConnection(host)
robots_url = "/"
connect.request("GET", robots_url)
response = connect.getresponse()
responsecode = response.status
print "Server Flags:", response.getheader("Server")
print "Date:", response.getheader("Date")
print "Cookie:", response.getheader("cookie")
print "Response Code:", responsecode

# Robots.txt
print ""
print "Robots.txt"
print "<----------------------------------------------->"
connect = httplib.HTTPConnection(host)
robots_url = "/robots.txt"
connect.request("GET", robots_url)
response = connect.getresponse()
# basic error checking
if response.status != 200:
	print 'Error!', 'status code:', response.status
robots = response.read()
print robots
save = raw_input("(s)ave / (c)ontinue / (q)uit: ")

if save == "q":
	print ">> quitting..."
	sys.exit(1)
elif save == "s":
	print ">> saving to ./robots.txt"
	output = open("robots.txt", 'w')
	output.write(robots)
	output.close()
else:
	 print "onward..."

# crossdomain.xml
print ""
print "crossdomain.xml"
print "<----------------------------------------------->"
connect = httplib.HTTPConnection(host)
cdxml_url = "/crossdomain.xml"
connect.request("GET", cdxml_url)
response = connect.getresponse()
# basic error checking
if response.status != 200:
	print 'Error!', 'status code:', response.status

cdxml = response.read()
print cdxml
save = raw_input("(s)ave / (c)ontinue / (q)uit: ")

if save == "q":
	print ">> quitting..."
	sys.exit(1)
elif save == "s":
	print ">> saving to ./crossdomain.xml"
	output = open("crossdomain.xml", 'w')
	output.write(cdxml)
	output.close()
else:
	 print "onward..."
	

print ""
print "all done"
print "bugs: code@zonbi.org"