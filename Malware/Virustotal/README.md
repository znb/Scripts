Virus Total stuff
=================

Virus total stuff...mostly for their public API


 * vtevilsubmit.py - Submit or check files and URLs to the VT API.
 * vthashcheck.py - New hash checker for v2 API using the requests module
 * vtbulkcheck.py - Simple bulk hash checker (Note: API rate limiting)



vtevilcheck_v2.py
-----------------

This script takes a number of arguments. 

 * -h for basic help
 * -k to specify a different key file to ~/.virustotal.key
 * -H to check VT for a specific hash
 * -r to check VT for a resource. This can be a hash, scan ID value or a URL
 * -f to submit a file to VT for scanning
 * -u to submit a URL to VT for scanning
 * -i to get a report on an IP address
 * -d to get a report on a domain name 
 * -b to do a bulk hash check (Note: API rate limiting)


It's worth noting that both the file and URL submission checks will perform a 
precheck on VT to see if the file or URL has been submitted already. 



Bugs can go to code at zonbi dot org.


Thanks to the VT crew for being full of awesome

