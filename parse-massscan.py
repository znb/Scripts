#!/usr/bin/python
# Simple mass scan output generator 
# Hacked from http://blog.poultonfam.com/brad/2010/02/24/python-nmap-xml-parser/

import argparse
import sys
import datetime
import re
from xml.dom.minidom import parse, parseString


def dosomeworkslacker(axmlfile, acsvfile):
    """Stuff"""
    print "Let's get this party started"
    print "Input from: " + axmlfile
    output = open('output.csv', 'a')
    print "Output going to: output.csv" 
    output.write('\n<----started at: ')

    now = datetime.datetime.now()
    print ""
    output.write(now.strftime("%Y-%m-%d %H:%M"))
    output.write(' ----->\n')

    print "Opening scan file for parsing"
    dom = parse(axmlfile)
    nmapvars = {}
    hostname = ''
    os = ''
    args = ''
    date = ''
    port = []
    name = []
    product = []
    version = []
    extrainfo = []
    portstate = []
    goodXML = []

    scaninfo = dom.getElementsByTagName('nmaprun')[0]
    date = scaninfo.getAttribute("startstr")
    args = scaninfo.getAttribute('args')

    dom.unlink()
    output.close()


def translateXml(node):
    """translate our XML stuff into something useful"""
    #if node.nodeName == 'hostname':
    #
    #    hostname = node.getAttribute('name')
    #    output.write(node.getAttribute('name'))
    #    output.write(':')

    #elif node.nodeName == 'address':

    if 'ip' in node.getAttribute('addrtype'):
        output.write('\n')
        ipaddr = node.getAttribute('addr')
        output.write(node.getAttribute('addr'))
        output.write(' >> ')

    elif node.nodeName == "port":
        port.append(node.getAttribute("portid"))
        output.write(node.getAttribute("portid"))

    elif node.nodeName == "state":

        isopen = node.getAttribute('state')
        portstate.append(node.getAttribute('state'))
        output.write(node.getAttribute('state'))
        output.write(',')
        #if isopen == "open":
        #    portstate.append(node.getAttribute('state'))
        #    output.write(node.getAttribute('state'))
        #    output.write(',')
        #else:
        #    pass

    elif node.nodeName == "service":

        name.append(node.getAttribute("name"))
        output.write(node.getAttribute('name'))
        output.write(',')
        product.append(node.getAttribute("product"))
        output.write(node.getAttribute('product'))
        output.write(',')
        version.append(node.getAttribute("version"))
        output.write(node.getAttribute('version'))
        output.write(',')
        extrainfo.append(node.getAttribute("extrainfo"))
        output.write(node.getAttribute('extrainfo'))
        output.write(',')

def parsethisbitch():
    """Do some XML parsing"""
    print "Parsing this bitch"
    for node in dom.getElementsByTagName('host'):
        for subnode in node.childNodes: 
            if subnode.attributes is not None: 
                translateXml(subnode) 
                if len(subnode.childNodes) > 0: 
                    for subsubnode in subnode.childNodes: 
                        if subsubnode.attributes is not None: 
                            translateXml(subsubnode) 
                            if len(subsubnode.childNodes) > 0:
                                for subsubsubnode in subsubnode.childNodes:
                                    if subsubsubnode.attributes is not None:
                                        translateXml(subsubsubnode) 



def __main__():

    parser = argparse.ArgumentParser(description='basic output parser', usage='%(prog)s -i input.xml -o output.csv')
    parser.add_argument('--input', '-i', dest='infile', help='file to input xml from')
    parser.add_argument('--output', '-o', dest='outfile', default='output.csv', help='file to output csv to')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    axmlfile = args.infile
    acsvfile = args.outfile

    if not args.infile:
        sys.exit(parser.print_help())

    dosomeworkslacker(axmlfile, acsvfile)

if __name__ == '__main__':
    __main__()

