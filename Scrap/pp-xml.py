#!/usr/bin/python
# Pretty print an XML file

import sys
import xml.dom.minidom

try:
    xml_fname = sys.argv[1]
except:
    sys.exit("something has gone horribly wrong")


xml = xml.dom.minidom.parse(xml_fname)
pretty_xml_as_string = xml.toprettyxml()
print pretty_xml_as_string
