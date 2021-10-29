#!/usr/bin.python
# Simple script to pull down a remote URL for analysis with Thug

import argparse
import sys
import os
import hashlib
try:
    import requests
except:
    sys.exit("You need the requests library")


def hash_url_file(hashme):
    """Return a hash of the given url file"""
    file = open(hashme, 'rb')
    m = hashlib.md5()
    m.update(file.read())
    digest = m.hexdigest()
    file.close()

    return digest


def dup_check(fullpath, adest, r):
    """Check if we've already pulled down a copy"""
    scanned_file = fullpath + "-SCANNED"
    new_hash_file = fullpath + "-SCANME"
    tmp_hash_file = fullpath + "-TMP"
    check = os.path.isfile(scanned_file)
    if check is True:
        old_hash = hash_url_file(scanned_file)
        with open(tmp_hash_file, 'w') as tmp:
            tmp.write(r.content)
            tmp.close()
        new_hash = hash_url_file(tmp_hash_file)
        if old_hash == new_hash:
            os.remove(scanned_file)
            os.rename(tmp_hash_file, scanned_file)
            dup_check = 2
        elif old_hash != new_hash:
            os.remove(scanned_file)
            os.rename(tmp_hash_file, new_hash_file)
            dup_check = 1
    else:
        with open(new_hash_file, 'w') as new:
            new.write(r.content)
            new.close()
        dup_check = 0

    return dup_check


def url_pull(url, adest):
    """Pull down our URLs for review"""
    print " * Checking: " + url,
    global md5url
    md5url = hashlib.md5(url).hexdigest()
    headers = {"User-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    r = requests.get(url, headers=headers)
    fullpath = adest + "/" + md5url
    # Check if we have already scanned the file
    dupcheck = dup_check(fullpath, adest, r)
    scanning = 0
    if dupcheck == 0:
        scanning += 1
        print " >> No existing hashes. \t[ SCANNING ]"
    elif dupcheck == 1:
        scanning += 1
        print " >> Site content changed. \t[ SCANNING ]"
    elif dupcheck == 2:
        print " >> Site content hasn't changed. \t[ NOT SCANNING ]"

    return scanning


def load_file(afile, adest):
    """Load our URLs from file"""
    if not os.path.exists(adest):
        os.makedirs(adest)
    total_scans = 0
    with open(afile, 'r') as fh:
        for url in fh:
            clean_url = url.rstrip()
            # Get our URL for scanning
            scanning = url_pull(clean_url, adest)
            if scanning == 1:
                total_scans += 1
    print "\n[ Dumped URLs to file for Thug Analysis: " + adest + "\tTotal scans: " + str(total_scans) + " ]"
    # Nasty hack for Thug
    if total_scans >= 1:
        tmp_thug = "/tmp/.thugme.txt"
        with open(tmp_thug, 'w') as tmpfile:
            tmpfile.write("scan")
        tmpfile.close()
    else:
        pass


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='URL Puller')
    parser.add_argument('--file', '-f', dest='file', help='File with URLs to pull down')
    parser.add_argument('--dest', '-d', dest='dest', default='/tmp/', help='Directory directory to dump to')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    global adest
    adest = args.dest

    if not args.file:
        sys.exit(parser.print_help())
    else:
        print "\n\n[ Thug URL Dumper ]\n"
        load_file(afile, adest)

if __name__ == '__main__':
    __main__()