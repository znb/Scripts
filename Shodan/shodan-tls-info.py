#!/usr/bin/python
# Pull TLS certification information for IP

import shodan
import sys

try:
    host = sys.argv[1]
except:
    sys.exit("[ERROR] We need an IP to lookup")

print "[HOST] " + host

SHODAN_API_KEY = "DEAR_LORD_I_POSTED_MY_API_KEY"

api = shodan.Shodan(SHODAN_API_KEY)
host_data = api.host(host)
print "Last update: " + host_data['last_update']

data = host_data['data']
tlsdata = data[0]['ssl']
print "Expired: " + str(tlsdata['cert']['expired'])
print "Expires: " + tlsdata['cert']['expires']
