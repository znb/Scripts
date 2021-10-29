#!/usr/bin/python
# Bulk Google Safe Browsing API lookup and reporter

import argparse
import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
import urllib
try:
    import requests
except:
    print "You need the requests library"


def load_apikey():
    """Load our API key from file"""
    fullpath = os.getenv("HOME")
    try:
        with open(fullpath + '/.googlesafe.key', 'r') as keyfile:
            for line in keyfile:
                googlekey = line.rstrip()
                keyfile.close()
                return googlekey
    except: 
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.googlesafe.key")


def load_config(aconfig):
    """Load our config settings from file"""
    try:
        jconfig=open(aconfig)
    except:
        sys.exit(" ** [Error: Problem loading config file]")
    data = json.load(jconfig)
    jconfig.close()

    global mailfrom
    mailfrom = data["from"]
    global mailto
    mailto = data["to"]
    global subject
    subject = data["subject"]
    global tmpfile
    tmpfile = data["tmpfile"]
    global smtpserver
    smtpserver = data["smtpserver"]

def send_report():
    """Email our report"""
    with open(tmpfile, 'r') as fp:
        # Create a text/plain message
        msg = MIMEText(fp.read())
        fp.close()
    msg['Subject'] = subject
    msg['From'] = mailfrom
    msg['To'] = mailto


    print "\nSending report to: " + mailto,
    s = smtplib.SMTP(smtpserver)
    s.sendmail(mailfrom, [mailto], msg.as_string())
    s.quit()
    os.remove(tmpfile)
    print "...done."


def google_lookup(url):
    """Check Google for our urls"""
    googlekey = load_apikey()
    encoded_url = urllib.quote_plus(url)
    google_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=firefox&apikey=" + \
                    googlekey + "&appver=1.0&pver=3.0&url=" + \
                    encoded_url
    try:
        # Simple GET request to Google
        resp = requests.get(google_url)
    except:
        sys.exit("Problem with HTTP request to Google")
    scode = resp.status_code
    if scode == 204:
        return 0
    elif scode == 200:
        return 200
    elif scode == 400:
        sys.exit("Error: 400 Bad Request")
    elif scode == 401:
        sys.exit("Error: 401 API Key problem")
    elif scode == 403:
        sys.exit("Error: 403 API Key problem")
    elif scode == 503:
        sys.exit("Error: 503 Service unavailable")


def load_files(afile, quiet):
    """Load urls from file"""
    print "Checking Google Safe Browsing..."
    print "Loading configuration",
    load_config(aconfig)
    print "...ok\n"
    malreport = []
    with open(afile, 'r') as fh:
        lines = 0
        checked = 0
        good = 0
        for line in fh:
            lines += 1
            url = line.rstrip()
            gsb = google_lookup(url)
            checked += 1
            if gsb == 0:
                if quiet == "1":
                    good += 1
                    pass
                else:
                    good += 1
                    print url + " [ok]"
            elif gsb == 200:
                maltext = url + " [MALICIOUS]"
                malreport.append(maltext)
                print url + " [MALICIOUS]"

    if checked == good:
        print "\n[ No Malicious Links Reported ]"
    else:
        # I know this can be done better.
        with open(tmpfile, 'w') as reportfile:
            for line in malreport:
                reportfile.write(line)
                reportfile.write("\n")
            reportfile.close()
        send_report()
    print "\n[ URLs checked: " + str(lines) + " ]"
    print "[ Analysis Complete ]"


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Google Safe Browsing Check and Notify System')
    parser.add_argument('--file', '-f', dest='file', help='File to pull URLs from')
    parser.add_argument('--config', '-c', dest='config', help='Configuration file to pull settings from')
    parser.add_argument('--quiet', '-q', dest='quiet', action='store_true', help='Less verbose')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    global aconfig
    aconfig = args.config
    aquiet = args.quiet

    if not (args.file or args.config):
        sys.exit(parser.print_help())
    else:
        if args.quiet:
            quiet = "1"
            load_files(afile, quiet)
        else:
            quiet = "0"
            load_files(afile, quiet)


if __name__ == '__main__':
    __main__()
