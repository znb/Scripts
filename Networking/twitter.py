#!/usr/bin/python
# Simple Tweet script 

import os
import argparse
import sys
import twitter
import re


def send_tweet(atweet):
    """Send tweets"""
    # Gotta be a better way to do this
    keys = []
    keys = load_apikey()
    consumer_key = keys[0]
    consumer_secret = keys[1]
    access_token_key = keys[2]
    access_token_secret = keys[3]
    print "Should we send: '" + atweet + "' ?"
    query = raw_input("(y)/(n): ").lower()
    if query == "y":
        api = twitter.Api()
        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
        status = api.PostUpdate(atweet)
        print status.text    
    else:
        sys.exit("Not tweeting :(")
    

def load_apikey():
    """Load our API keys from file"""
    print "Loading API keys"
    fullpath = os.getenv("HOME")
    try:
        keyfile = open(fullpath + '/.twitter.key', 'r')
    except: 
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.twitter.key")

    for line in keyfile:
        # This is fucking ugly
        if re.match("ConsumerKey", line):
            ConsumerKey = line
        if re.match("ConsumerSecret", line):
            ConsumerSecret = line
        if re.match("AccessTokenKey", line):
            AccessTokenKey = line
        if re.match("AccessTokenSecret", line):
            AccessTokenSecret = line

    keyfile.close()
    return ConsumerKey, ConsumerSecret, AccessTokenKey, AccessTokenSecret
    

def main():
    """Basic menu system"""
    parser = argparse.ArgumentParser(description='basic tweet sender', usage='%(prog)s -t tweet')
    parser.add_argument('--tweet', '-t', dest='tweet', help='tweet to send')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    atweet = args.tweet

    if not args.tweet:
        sys.exit(parser.print_help())

    send_tweet(atweet)

if __name__ == '__main__':
    main()