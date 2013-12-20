#!/usr/bin/python
# Simple hash creator because I'm lazy

import hashlib
import sys
import argparse


def gethash(afile, hashtype):
    """Get the hash value for our file"""
    print "Hashing file: " + afile + "  (" + hashtype + ")"
    try:
        data = open(afile, 'rb').read()
    except IOError, e:
        sys.exit(e)
    if hashtype == "all":
        for ht in ['md5', 'sha1', 'sha256']:
            md5 = hashlib.md5(data).hexdigest()
            sha1 = hashlib.sha1(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
        print "MD5: %s" % md5
        print "SHA1: %s" % sha1
        print "SHA256: %s" % sha256
    elif hashtype == "md5":
        hashout = hashlib.md5(data).hexdigest()
        print "%s: %s" % (hashtype, hashout)
    elif hashtype == "sha1":
        hashout = hashlib.sha1(data).hexdigest()
        print "%s: %s" % (hashtype, hashout)
    elif hashtype == "sha256":
        hashout = hashlib.sha256(data).hexdigest()
        print "%s: %s" % (hashtype, hashout)
 

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic hashing tool', usage='%(prog)s -f file')
    parser.add_argument('--file', '-f', dest='file', help='file to hash')
    parser.add_argument('--md5', '-m', dest='md5', action="store_true", help='just print the MD5')
    parser.add_argument('--sha1', '-1', dest='sha1', action="store_true", help='just print the SHA1')
    parser.add_argument('--sha256', '-2', dest='sha256', action="store_true", help='just print the SHA256')
    parser.add_argument('--all', '-a', dest='all', action="store_true", help='print all the hash values for a file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    amd5 = args.md5
    asha1 = args.sha1
    asha256 = args.sha256

    if not args.file:
        sys.exit(parser.print_help())

    if amd5:
        gethash(afile, hashtype="md5")
    elif asha1:
        gethash(afile, hashtype="sha1")
    elif asha256:
        gethash(afile, hashtype="sha256")
    else:
        gethash(afile, hashtype="all")

if __name__ == '__main__':
    __main__()
