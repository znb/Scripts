#!/usr/bin/python

# simple script to expand a short url using the http://longurl.org API
# Matt E <code@zonbi.org>

import sys
from optparse import OptionParser
import urllib
import httplib

surl = ""

# basic menu system 
def menu():
        
        p = OptionParser(usage="%prog -u http://t.co/whatever", version="%prog 0.1a")
        
        p.add_option("-u", 
                    action="store", 
                    type="string", 
                    dest="shorturl", 
                    help="Short URL to expand")
        
        options, args = p.parse_args()
        # I need to fix this. It's not working quite right
        # (It's not taking blank arguements are blank arguements)
        if len(args) >= 1:
                print "<< Link Expander v0.1a >>"
                p.print_help()
                sys.exit()
        else:
            global surl
            surl = options.shorturl     
                    

# send the short URL off for parsing
def urlparse():
    
    print "expanding: ", surl
    # send the URL for parsing
    headers = { "User-Agent" :"shorturl-parser-v1" }
    params = urllib.urlencode({ 'url' : surl, 'format' : "php" })  
    c = urllib.urlopen("http://api.longurl.org/v2/expand?%s" % params)
    # parse out the good stuff (perhaps this can get cleaned up)
    x = c.read()
    longurl = x[26:-3]
    print "long url: ", longurl 
    c.close()
    
menu()
urlparse()