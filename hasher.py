#!/usr/bin/python
# Simple hash creator because I'm lazy
# Matt Erasmus <code@zonbi.org>

import hashlib
import sys
#from ssdeep import ssdeep

if len(sys.argv) != 3:
        print 'Usage: %s <file> <output>' % sys.argv[0]
        sys.exit(1)

hashme = sys.argv[1]
hashfile = sys.argv[2]

print '>> GENERATING :', hashme

data = open(hashme, "rb").read()
md5 = hashlib.md5(data).hexdigest()
sha1 = hashlib.sha1(data).hexdigest()
#s = ssdeep()
#ssdeep = s.hashfile(hashme)

print "<~-----------------------------------------------------~>"
print "MD5: ", md5
print "SHA1: ", sha1
#print "SSDEEP: ", ssdeep
print "SSDEEP: COMING SOON TO A CINEMA NEAR YOU"
print "<~-----------------------------------------------------~>"

# I'm sure this can be done better 
output = open(hashfile, "w")
output.write("Hashes for: ")
output.write(hashme)
output.write("\n")
output.write("----------------------------")
output.write("\n")
output.write("MD5: ")
output.write(md5)
output.write("\n")
output.write("SHA1: ")
output.write(sha1)
output.write("\n")
output.write("SSDEEP: ")
output.write("SSDEEP: COMING SOON TO A CINEMA NEAR YOU")
output.write(sha1)
output.write("\n")

output.close()

print ""
print ">> Your hashes are saved in", hashfile
print "                            EOF <<"

