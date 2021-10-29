#!/usr/bin/python

# Simple PHP malware decoder.

import argparse
import sys
import base64
import zlib
import codecs


def base64_decode(arg_file):
    """Base64 decode the blob of data"""
    print " decoding base64 data..."
    inputfile = open(arg_file, 'r')
    for line in inputfile:
        to_rot13 = base64.b64decode(line)
    inputfile.close()
    unrot13(to_rot13)


def unrot13(to_rot13):
    """Derot13 the data passed to us from the base64 decode process"""
    print " rotating 13 the other way..."
    unrot13_out = codecs.decode(to_rot13, 'rot13')
    gzip_inflate(unrot13_out)


def gzip_inflate(unrot13_out):
    """Gzip inflate the data from the unrot13 process"""
    print " inflating the data..."
    gzip_output = zlib.decompress(unrot13_out)
    printoutput(gzip_output)


def printoutput(gzip_output, arg_output):
    """Print the output out to the console"""
    print " printing output"
    output = file(arg_output, 'w')
    output.write(gzip_output)
    output.close()
    print "file written to " + arg_output
    print "we're done here."


def __main__():
    """Get this party started here
    Basic menu system"""
    parser = argparse.ArgumentParser(description='basic menu system', usage='%(prog)s -f file')
    parser.add_argument('--file', '-f', dest='filein', help='file to examine')
    parser.add_argument('--output', '-o', dest='fileout', help='write to file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    arg_file = args.filein
    arg_output = args.fileout

    if not args.filein:
        sys.exit(parser.print_help())

    print "examining file "
    print "(" + arg_file + ")"
    base64_decode(arg_file)


if __name__ == '__main__':
    __main__()
