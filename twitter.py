#!/usr/bin/python
# Simple Tweet script 

import os
import argparse
import sys
import twitter
import re


def send_tweet():
    """Send tweets"""
    print ""
    load_apikey()
    print ConsumerKey, ConsumerSecret, AccessTokenKey, AccessTokenSecret
    sys.exit("bailing out")
    print "sending tweet: '" + arg_tweet + "'"
    api = twitter.Api()
    api = twitter.Api(consumer_key=ConsumerKey, consumer_secret=ConsumerSecret, access_token_key=AccessTokenKey, access_token_secret=AccessTokenSecret)
    status = api.PostUpdate(tweet)
    print status.text


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

    send_tweet()

if __name__ == '__main__':
    main()