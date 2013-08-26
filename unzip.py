#!/usr/bin/python

# Simple Zip file extraction

import zipfile
import os

enc_archive = zipfile.ZipFile("C:\sample\example.zip")
dest = "C:\sample"
password = "infected"
new_sample = "C:\sample\malware.exe"

print "\nSample contents\n"
files = enc_archive.namelist()
for x in files:
		print "> " + x

		print ""

		print "Extracting sample to " + dest
		for x in files:
				enc_archive.extract(x, dest, password)
				enc_archive.close()

				print "Renaming sample to something friendly"
				old_sample = dest + "\\" + x
				print old_sample + " > " + new_sample
				os.rename(old_sample, new_sample)

				print "\nWe're done here"
