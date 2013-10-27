#!/usr/bin/python
# Grab my external IP address
# parts of this was borrowed from 
# http://johnklann.com/python-how-to-get-external-ip-address/

import urllib
import re
from socket import gethostbyaddr

URL="http://ipchicken.com"

request = urllib.urlopen(URL).read()
ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', request)
hostname = gethostbyaddr(str((ip[0])))
print "[*] external ip: " + str(ip[0])
print "[*] hostname: " + str(hostname[0])

