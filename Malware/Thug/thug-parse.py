#!/usr/bin/python
# Pull links from a Thug JSON report and check them against VT and GSB

import argparse
import os
import sys
import json
import urllib
import time
try:
    import requests
except:
    print "You need the requests library"


def load_gsbkey():
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


def google_lookup(url):
    """Check Google for our urls"""
    googlekey = load_gsbkey()
    encoded_url = urllib.quote_plus(url)
    google_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=firefox&apikey=" + \
                 googlekey + "&appver=1.0&pver=3.0&url=" + \
                 encoded_url
    try:
        resp = requests.get(google_url)
    except:
        sys.exit("Error with request to Google")
    scode = resp.status_code
    if scode == 204:
        return 204
    if scode == 200:
        body = resp.text
        return body
    elif scode == 400:
        return 400
    elif scode == 401:
        sys.exit("[Error: API key problem]")
    elif scode == 403:
        sys.exit("[Error: API key problem]")
    elif scode == 503:
        sys.exit("[Error: Service unavailable]")


def load_vtkey():
    """Load our API key from file"""
    fullpath = os.getenv("HOME")
    try:
        keyfile = open(fullpath + '/.virustotal.key', 'r')
    except:
        sys.exit("** ERROR ** \n> Key file not found. Please check ~/.virustotal.key")

    for line in keyfile:
        vtkey = line.rstrip()
    keyfile.close()

    return vtkey


def virustotal_url_lookup(url):
    """Check a URL against VT"""
    vtkey = load_vtkey()
    vturl = "https://www.virustotal.com/vtapi/v2/url/report"
    parameters = {"resource": url, "apikey": vtkey}
    try:
        resp = requests.get(vturl, params=parameters)
    except:
        sys.exit("Problem with the HTTP request to VT")

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        evilrating = 0
        pass
    else:
        evilness = report.get("positives", {})
        webutation = report.get("scans", {}).get("Webutation").get("result")
        if evilness == 0:
            pass
            evilrating = evilness
        elif evilness == 1:
            print "Possibly evil",
            if webutation:
                print "(Evilness from Webutation)"
            evilrating = evilness
        elif evilness >= 2:
            evilrating = evilness

    return evilrating


def load_report(areport):
    """Load our report"""
    print "\n * Loading report: ",
    try:
        jreport = open(areport)
    except:
        sys.exit(" ** [Error: Problem loading report]")
    data = json.load(jreport)
    jreport.close()
    conns = data["connections"]
    count = 0
    for conn in conns:
        count += 1
    print str(count) + " URLs"

    return conns


def no_lookups(areport, aoutput):
    """Don't perform lookups just dump the URLS"""
    conns = load_report(areport)
    count = 0
    url_list = []
    for conn in conns:
        url = conn["destination"]
        if url is None:
            pass
        elif url == "javascript:\'\'":
            pass
        elif url not in url_list:
            count += 1
            url_list.append(url)
    outputf = aoutput + "/urls-for-lookup.txt"
    with open(outputf, 'w') as dump_file:
        for url in url_list:
            dump_file.write(url + "\n")
        dump_file.close()
    print "\n[ Complete: " + str(count) + " to scan ]"


def perform_lookups(areport, aoutput):
    """Perform our lookups and report"""
    conns = load_report(areport)
    count = 0
    url_list = []
    for conn in conns:
        url = conn["destination"]
        if url is None:
            pass
        elif url == "javascript:\'\'":
            pass
        elif url not in url_list:
            count += 1
            url_list.append(url)

    glr = google_lookups(url_list, aoutput)
    now = time.strftime("%Y-%m-%d %H:%M")
    print "\n [ Analysis Complete: " + now + " Lookups >> GSB:" + str(gsburlcount) + " VT: " + str(vturlcount) + " ]\n"


def google_lookups(url_list, aoutput):
    """Perform various Google lookups"""
    # Do a GSB lookup for all URLs
    print "\n * Google Safe Browsing Lookup on URLs\n"
    count = 0
    exported_evil = 0
    global vturlcount
    vturlcount = 0
    eyewitness = []
    for url in url_list:
        count += 1
        gsl = google_lookup(url)
        if gsl == 204:
            pass
        elif gsl == 400:
            print url
            print "[Error 400: Bad Request]"
        elif gsl == "malware":
            print " !! " + url + " >> Google reported malicious...checking VT",
            vturlcount += 1
            vtl = virustotal_url_lookup(url)
            print "[ Detection: " + str(vtl) + "/52 ]"
            eyewitness.append(url)
            exported_evil = 1

    if not eyewitness:
        pass
    else:
        print "\n * Dumping URLs for Eyewitness",
        eyewitnessf = aoutput + "/eyewitness.txt"
        with open(eyewitnessf, 'w') as fh:
            for url in eyewitness:
                fh.write(url)
            fh.close
        print "..." + eyewitnessf

    global gsburlcount
    gsburlcount = count

    return exported_evil


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Thug report parser')
    parser.add_argument('--report', '-r', dest='report', help='Report to parse')
    parser.add_argument('--no-lookups', '-n', dest='nolookups', action='store_true', help='No GSB Lookups just dump to file')
    parser.add_argument('--output', '-o', dest='output', default='/tmp', help='Output directory')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    areport = args.report
    global aoutput
    aoutput = args.output
    anolookups = args.nolookups

    if not (args.report or args.nolookups):
        sys.exit(parser.print_help())
    elif args.nolookups:
        print "\n\n[ Malicious Checks Starting ]"
        no_lookups(areport, aoutput)
    else:
        print "\n\n[ Malicious Checks Starting ]"
        perform_lookups(areport, aoutput)


if __name__ == '__main__':
    __main__()

