#!/usr/bin/python
# Simple file/url uploader for Virustotal using the requests module
# It expects your VT API Key in ~/.virustotal.key


import os
import argparse
import sys
import requests
import hashlib


def bulkcheck(abulk):
    """Bulk checker against VT"""
    vtkey = load_apikey()
    print "Checking hashes in file: " + abulk
    try:
        fhandle = open(abulk, 'r')
        nlines = sum(1 for line in fhandle)
        if nlines > 4:
            print "*** WARNING: Bulk checks are limited to 4 per minute on the public API ***"
            pass
    except IOError, e:
        sys.exit("Error: %s" % e)

    vturl = "https://www.virustotal.com/vtapi/v2/file/report"
    fhandle = open(abulk, 'r')
    hashes = fhandle.readlines()
    for hash in hashes:
        try:
            hash = hash.rstrip()
            parameters = {"resource": hash, "apikey": vtkey }
            resp = requests.get(vturl, params=parameters)
            report = resp.json()
            resp_code = report.get("response_code", {})
            if resp_code == 0:
                sys.exit("Exiting. \nGot an unexpected error back from VT")
            evilness = report.get("positives", {})
            totaleng = report.get("total", {})
            print hash + " Evilness: " + str(evilness) + "/" + str(totaleng)
        except ValueError, e:
            sys.exit("Error: %s" % e)

def filesubmit(asubfile):
    """Check a domain name against VT"""
    vtkey = load_apikey()

    try:
        filehandle = open(asubfile, 'rb').read()
    except:
        sys.exit("** Error: Supply a file for upload")

    print "Calculating hash for : " + asubfile
    filehash = hashlib.md5(filehandle).hexdigest()
    print "Checking file: " + asubfile
    print "Checking for existing scan results"
    precheck = check_resource(filehash, rtype="FILE")
    if precheck == True:
        sys.exit()
    else:
        pass
    print "Uploading file to VT"
    vturl = "https://www.virustotal.com/vtapi/v2/file/scan"
    payload = {"apikey": vtkey, "file": (asubfile, filehandle) }
    try:
        resp = requests.post(vturl, files=payload)
    except:
        sys.exit("Unexpected error 31")
    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Nothing found for file: " + asubfile)

    verb_msg = report.get("verbose_msg", {})
    scan_date = report.get("scan_date", {})
    scan_id = report.get("scan_id", {})
    permalink = report.get("permalink", {})
    print "Message: " + verb_msg
    print "Scan date: " + str(scan_date)
    print "Scan id: " + str(scan_id)
    print "\nPermalink: " + permalink
    


def check_domain(asubdomain):
    """Check a domain name against VT"""
    vtkey = load_apikey()
    print "Checking IP: " + asubdomain
    vturl = "https://www.virustotal.com/vtapi/v2/domain/report"
    parameters = {"domain": asubdomain, "apikey": vtkey }
    try:
        resp = requests.get(vturl, params=parameters)
    except:
        sys.exit()
    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Nothing found for domain: " + asubdomain) 

    verb_msg = report.get("verbose_msg", {})
    print "Message: " + verb_msg
    print "\nPassive DNS report for: " + asubdomain + "\n"
    hostlist = report.get("resolutions", {})
    for hosts in hostlist:
         lastseen = hosts['last_resolved']
         host = hosts['ip_address']
         print "IP Address: " + host + "\tLast seen: " + lastseen
    
    print "\nDetected URLS\n"
    url_list = report.get("detected_urls", {})
    for url in url_list:
        detectedurl = url['url']
        evilness = url['positives']
        totalness = url['total']
        scan_date = url['scan_date']
        print "URL Detected: " + detectedurl
        print "\_-> Evilness: " + str(int(evilness)) + "/" + str(int(totalness)),
        print "Scan date: " + str(scan_date)     


def check_ip(asubip):
    """Check an IP against VT"""
    vtkey = load_apikey()
    print "Checking IP: " + asubip
    vturl = "https://www.virustotal.com/vtapi/v2/ip-address/report"
    parameters = {"ip": asubip, "apikey": vtkey }
    try:
        resp = requests.get(vturl, params=parameters)
    except:
        sys.exit()
    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Exiting. IP not in dataset.")

    verb_msg = report.get("verbose_msg", {})
    print "Message: " + verb_msg
    print "\nPassive DNS report for: " + asubip + "\n"
    hostlist = report.get("resolutions", {})
    for hosts in hostlist:
         lastseen = hosts['last_resolved']
         host = hosts['hostname']
         print "Hostname: " + host + "\tLast seen: " + lastseen

    
    print "\nDetected URLS\n"
    url_list = report.get("detected_urls", {})
    for url in url_list:
        detectedurl = url['url']
        evilness = url['positives']
        totalness = url['total']
        scan_date = url['scan_date']
        print "URL Detected: " + detectedurl + "\t(Evilness: " + str(int(evilness)) + "/" + str(int(totalness)) + "\t[Scan date: " + str(scan_date) + "])"


def urlsubmit(asuburl):
    """Submit a URL for scanning"""
    vtkey = load_apikey()
    print "Checking for existing scan results"
    precheck = check_resource(asuburl, rtype="URL")
    if precheck == True:
        sys.exit()
    else:
        pass

    print "Submitting URL: " + asuburl
    vturl = "https://www.virustotal.com/vtapi/v2/url/scan"
    payload = {"url": asuburl, "apikey": vtkey }
    try:
        resp = requests.post(vturl, data=payload)
    except:
        sys.exit()

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Exiting. \nGot an unexpected error back from VT")

    verb_msg = report.get("verbose_msg", {})
    scan_date = report.get("scan_date", {})
    scan_id = report.get("scan_id", {})
    permalink = report.get("permalink", {})
    print "Message: " + verb_msg
    print "Scan date: " + scan_date
    print "Scan id: " + scan_id
    print "\nPermalink: " + permalink
        

def check_resource(aresourceid, rtype):
    """Check VT for an existing scan ID/URL"""
    print "Resource check: " + rtype
    vtkey = load_apikey()
    print "Checking for resource ID: " + aresourceid
    vturl_url = "https://www.virustotal.com/vtapi/v2/url/report"
    vturl_file = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": aresourceid, "apikey": vtkey }
    if rtype == "URL":
        try:
            resp = requests.get(vturl_url, params=parameters)
        except:
            sys.exit("Error 31")
    elif rtype == "FILE":
        try: 
            resp = requests.get(vturl_file, params=parameters)
        except:
            sys.exit("Error 31")

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        print "No existing scan results found for: " + aresourceid
        return False
    else:
        print "Existing scan results for: " + aresourceid
        report = resp.json()
        verb_msg = report.get("verbose_msg", {})
        scan_date = report.get("scan_date", {})
        scan_url = report.get("url", {})    
        evilness = report.get("positives", {})
        totaleng = report.get("total", {})
        permalink = report.get("permalink", {})
        scanners = report.get("scans", {})
        print "\nMessage: " + verb_msg
        print "Scan date: " + scan_date
        print "Scan URL: " + str(scan_url)
        print "\nMalicious Detects: " + str(evilness) + "/" + str(totaleng)
        print "\nAV detections: ",
        if rtype == "FILE":
            print "file report.\n"
            detected = []
            undetected = []
            for scanner in scanners:
                avreport = report.get("scans", {}).get(scanner, {}).get("result")
                avversion = report.get("scans", {}).get(scanner, {}).get("version")
                if avreport == None:
                    undetected.append(scanner + " / " + str(avversion))
                else:
                    detected.append(scanner + " / " + str(avversion) + "\t\tDetection: " + str(avreport))

            print "Successful detections: "
            for good in detected:
                print "\t" + good

            print "\nUnsuccessful at detection: "
            for bad in undetected:
                print "\t" + bad
        else:
            print "URL report.\n"
            detected = []
            undetected = []
            for scanner in scanners:
                avreport = report.get("scans", {}).get(scanner, {}).get("result")
                avversion = report.get("scans", {}).get(scanner, {}).get("version")
                if avreport == "clean site":
                    detected.append(scanner + " / " + str(avversion) + "\t\tDetection: " + str(avreport))
                else:
                    undetected.append(scanner + " / " + str(avversion))

            print "Detections: "
            for good in detected:
                print "\t" + good

            print "\nNo detections: "
            for bad in undetected:
                print "\t" + bad
            
        print "\nPermalink: " + permalink
        return True

def check_hash(ahash):
    """check hash against the virustotal.com database"""
    print "Checking VT API key"
    vtkey = load_apikey()
    print "Checking hash: ", ahash
    vturl = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": ahash, "apikey": vtkey }
    try:
        resp = requests.get(vturl, params=parameters)
    except:
        sys.exit()

    report = resp.json()
    resp_code = report.get("response_code", {})
    if resp_code == 0:
        sys.exit("Exiting. \nGot an unexpected error back from VT")
    verb_msg = report.get("verbose_msg", {})
    scan_date = report.get("scan_date", {})
    evilness = report.get("positives", {})
    totaleng = report.get("total", {})
    permalink = report.get("permalink", {})
    scanners = report.get("scans", {})
    print "Message: " + verb_msg
    print "Scan date: " + scan_date
    print "\nMalicious Detects: " + str(evilness) + "/" + str(totaleng)
    print "\nAV detections\n"
    detected = []
    undetected = []
    for scanner in scanners:
        avreport = report.get("scans", {}).get(scanner, {}).get("result")
        avversion = report.get("scans", {}).get(scanner, {}).get("version")
        if avreport == None:
            undetected.append(scanner + " / " + str(avversion))
        else:
            detected.append(scanner + " / " + str(avversion) + "\t\tDetection: " + str(avreport))

    print "Successful detections: "
    for good in detected:
        print "\t" + good

    print "\nUnsuccessful at detection: "
    for bad in undetected:
        print "\t" + bad

    print "\nPermalink: " + permalink


def load_apikey():
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


def __main__():
    """Lets get this party started"""        
    parser = argparse.ArgumentParser(description='Simple virustotal.com file/url/hash/ip/domain checker/uploader', usage='%(prog)s -h help')
    parser.add_argument('--hash', '-H', dest='hash', help='Check VT for this hash')
    parser.add_argument('--resourceid', '-r', dest='resourceid', help='Check VT for this scan ID/resource')
    parser.add_argument('--file', '-f', dest='subfile', help='Submit file for scanning')
    parser.add_argument('--url', '-u', dest='suburl', help='Submit URL for scanning')
    parser.add_argument('--ip', '-i', dest='subip', help='Submit an IP address for checking')
    parser.add_argument('--domain', '-d', dest='subdomain', help='Submit a domain name for checking')
    parser.add_argument('--bulk', '-b', dest='bulk', help='Submit hashes in file for hash checking')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()
    ahash = args.hash
    aresourceid = args.resourceid
    asubfile = args.subfile
    asuburl = args.suburl
    asubip = args.subip
    asubdomain = args.subdomain
    abulk = args.bulk

    if ahash:
        check_hash(ahash)
    elif aresourceid:
        check_resource(aresourceid, rtype="FILE")
    elif asubfile:
        filesubmit(asubfile)
    elif asuburl:
        urlsubmit(asuburl)
    elif asubip:
        check_ip(asubip)
    elif asubdomain:
        check_domain(asubdomain)
    elif abulk:
        bulkcheck(abulk)
    else:
        sys.exit(parser.print_help())        
    
        

if __name__ == "__main__":
        __main__()