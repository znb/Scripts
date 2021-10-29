#!/usr/bin/python
# no not really...this is a fucking ugly hack

import argparse
import sys


def splitstring(line, length):
    """split the raw string up into 2 byte chars"""
   
    sys.stdout.write("splitting, ")
    return ' '.join(line[i: i + length] for i in xrange(0, len(line), length))


def addsecretsauce(fin):
    """add hex chars so we can parse properly"""
    
    sys.stdout.write("hexing, ")
    return fin.replace(" ", "\\x")
    

def snipper(nomoresecrets):
    """tidying up unneeded crap"""

    match = '\\x'
    sys.stdout.write("tidying up, ")
    sys.stdout.write("topping, ")
    addheader = ''.join(('\\x', nomoresecrets))
    sys.stdout.write("tailing")
    removetail = addheader    
    return ('\n'.join((line[:-len(match)] if line.endswith(match) else line)
        for line in removetail.splitlines()))
   

def dumptofile(fout):
    """write our newly hacked file to our output file"""
    
    print "\ndumping to file: " + afileout
    fwrite = open(afileout, 'w')
    fwrite.write(fout)
    fwrite.close()


def doshit(line, afileout):
    """this is where we mix magic"""
    
    fin = splitstring(line, 2)
    trim = addsecretsauce(fin)
    fout = snipper(trim)
    sys.stdout.write("...done")
    dumptofile(fout)
    print "and I'm spent..."


def main():
    """get this party started"""

    parser = argparse.ArgumentParser(description='convert raw ascii to hex', usage='%(prog)s -f file')
    parser.add_argument('--input', '-i', dest='filein', help='input file')
    parser.add_argument('--output', '-o', dest='fileout', help='output file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afilein = args.filein
    global afileout
    afileout = args.fileout

    if not afilein:
        sys.exit(parser.print_help())

    print "Getting started..."
    parseme = open(afilein, 'r')
    for line in parseme:
        doshit(line, afileout)
    parseme.close()

if __name__ == '__main__':
    main()
