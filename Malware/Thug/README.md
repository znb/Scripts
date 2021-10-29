Thug
====

[Thug](https://github.com/buffer/thug/) is awesome. You should use Thug.
These are various scripts for Thug.

 * runthug.sh - lameass script for running Thug over multiple profiles
 * thug-parse.py - script to parse a report and do GSB/VT lookups on links
 * url-dumper.py - does a simple python get request on a list of urls and dumps to file
 * thugdor.sh - control script for Thugdor (tm)
 * spider.py - spider script to get the URLs for Thug

Thugdor
=======

Thugdor is (hopefully) going to be a neat little script that will:

 * get a list of URLs from file
 * do a simple Python GET request to pull down a local copy of the file
 * run thug on that local copy
 * pull out all links from the thug report
 * run Google Safe Browsing lookups on those links
 * run Virus Total lookups on anything GSB flags
 * run Virus Total lookups on any executable that's downloaded

