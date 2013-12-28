#!/usr/bin/python
# Simple mass scan output generator 
# Hacked from http://blog.poultonfam.com/brad/2010/02/24/python-nmap-xml-parser/

import datetime
import re
from xml.dom.minidom import parse, parseString


# start output file
print "Let's get this party started"
output = open('output.csv', 'a')
print "Output going to: output.csv" 
output.write('\n<----started at: ')

#get current time and put in output file
now = datetime.datetime.now()
print ""
output.write(now.strftime("%Y-%m-%d %H:%M"))
output.write(' ----->\n')

#setup variables
print "Opening scan file for parsing"
dom = parse('/tmp/testicle2.xml')
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


def translateXml(node):
    """translate our XML stuff into something useful"""
    if node.nodeName == 'hostname':

        hostname = node.getAttribute('name')
        output.write(node.getAttribute('name'))
        output.write(':')

    elif node.nodeName == 'address':

        if 'ip' in node.getAttribute('addrtype'):

            output.write('\n')
            ipaddr = node.getAttribute('addr')
            output.write(node.getAttribute('addr'))
            output.write(' >> ')

    elif node.nodeName == "port":

        #output.write(',')
        #output.write(',')
        #output.write(',')
        port.append(node.getAttribute("portid"))
        output.write(node.getAttribute("portid"))
        #output.write(',')

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


print hostname
dom.unlink()
output.close()