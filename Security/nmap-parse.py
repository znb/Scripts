#!/usr/bin/python
# Simple script to parse nmap XML and output to CSV
# Hacked from here: http://blog.poultonfam.com/brad/2010/02/24/python-nmap-xml-parser/

import argparse
import sys
import datetime
import re
from xml.dom.minidom import parse, parseString


def parse_xml(ainput, aoutput):
    """Parse our XML file"""
    print "Parsing",
    dom = parse(ainput)
    nmapvars = {}
    hostname = ''
    os = ''
    difficulty = ''
    args = ''
    date = ''
    port = []
    name = []
    protocol = []
    product = []
    product = []
    version = []
    extrainfo = []
    portstate = []
    goodXML = []

    scaninfo = dom.getElementsByTagName('nmaprun')[0]
    date = scaninfo.getAttribute("startstr")
    args = scaninfo.getAttribute('args')

    def translateXml(node):
        """This is a black hole to me :)"""
        if node.nodeName == 'hostname':
            hostname = node.getAttribute('name')
            noutput.write(node.getAttribute('name'))
            noutput.write(',')
        elif node.nodeName == 'address':
            if 'ip' in node.getAttribute('addrtype'):
                noutput.write('\n')
                ipaddr = node.getAttribute('addr')
                noutput.write(node.getAttribute('addr'))
                noutput.write(',')
        elif node.nodeName == "port":
            noutput.write('\n')
            noutput.write(',')
            noutput.write(',')
            noutput.write(',')
            port.append(node.getAttribute("portid"))
            noutput.write(node.getAttribute("portid"))
            noutput.write(',')
        elif node.nodeName == "state":
            portstate.append(node.getAttribute('state'))
            noutput.write(node.getAttribute('state'))
            noutput.write(',')
        elif node.nodeName == "service":
            name.append(node.getAttribute("name"))
            noutput.write(node.getAttribute('name'))
            noutput.write(',')
            product.append(node.getAttribute("product"))
            noutput.write(node.getAttribute('product'))
            noutput.write(',')
            version.append(node.getAttribute("version"))
            noutput.write(node.getAttribute('version'))
            noutput.write(',')
            extrainfo.append(node.getAttribute("extrainfo"))
            noutput.write(node.getAttribute('extrainfo'))
            noutput.write(',')
        elif node.nodeName == 'osmatch':
            os = node.getAttribute('name')
            noutput.write(node.getAttribute('name'))
            noutput.write(',')

    with open(aoutput, 'w') as noutput:
        noutput.write(',,,,,,,,,\n')
        noutput.write('IP Address,Host Name,All Ports Filtered,Open Ports,')
        noutput.write('State (O/C),Service,Version,Device Type,Running,OS Details\n')
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

    dom.unlink()
    noutput.close()
    print "...complete."


def load_file(ainput, aoutput):
    """Load our XML file"""
    try:
        with open(ainput, 'r') as xmlinput:
            print "Loading XML"
            parse_xml(ainput, aoutput)
    except:
        sys.exit("Error: Something has gone horribly wrong.")


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Nmap XML to CSV')
    parser.add_argument('--input-file', '-i', dest='input', help='XML file for input')
    parser.add_argument('--output-file', '-o', dest='output', default='nmap-output.csv', help='CSV output file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ainput = args.input
    aoutput = args.output

    if not args.input:
        sys.exit(parser.print_help())
    else:
        load_file(ainput, aoutput)


if __name__ == '__main__':
    __main__()

