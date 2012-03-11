#!/usr/bin/python
# Simple base64 decoder 
# Usage: pydecode.py <base64 string>
# Matt Erasmus <code@zonbi.org>

import sys

print ''
print 'decoded string: '
print ''

decodeme = sys.argv[1]

print decodeme.decode("base64")
