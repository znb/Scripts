Kippo is a great little SSH honey pot. It's available [here](https://code.google.com/p/kippo/)

Yes, it's probably pretty easy to fingerprint, but it's still interesting. 

These are just some scripts I pulled together to look at the Kippo log files.


kippo-report.sh
---------------

Just a quick and dirty bash script to pull useful info from your kippo log file.

Usage: 

 ./kippo-report.sh /path/to/your/kippo.log

Useful stuff in the report:

 * Total sessions
 * Successful logins
 * Total unique failed usernames
 * Failed usernames with frequency
 * Failed Username and Password Combinations
 * Successful Usernames with frequency
 * Passwords used in successful logins
 * Actual interactive sessions
 * Downloaded files



kippo-log-grabber.py
--------------------

This script will log into your Honeypot via ssh, run my other script and return the
results to the screen and/or dump to a text file. 

Usage:
 
 python ./kippo-log-grabber.py -H myfirstkippo.com -p 23 -u USERNAME -k /path/to/your/ssh/key -f /path/to/your/kippo.log

TODO: 
 
 * Add password logins
 * Maybe do a list of hosts to login and check ?
