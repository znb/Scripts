#!/bin/python
# This is a fork of Andrews work here: https://bitbucket.org/infosanity/kippoanalysis

import dbhash
import MySQLdb
import os

#os.system('clear')

# Database basics from:
## Berkley DB - http://stackoverflow.com/questions/37644/examining-berkeley-db-files-from-the-cli
## MySQL - http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python

# open Kippo' password file
passdb = dbhash.open('/opt/kippo-svn/data/pass.db')

# open connection to Kippo' MySQL database
kippodb = MySQLdb.connect(host='localhost', user='kippo', passwd='kipposecret', db='kippo')

cur = kippodb.cursor()

# Iterate through password file
for passwd, junk in passdb.iteritems():
	passwd = str(passwd)

	# need to insert $passwd into SQL string
	creationSessionSQL = "SELECT session FROM input WHERE input = '%s'" % passwd
	
	cur.execute(creationSessionSQL)

	for row in cur.fetchall():
		sessionID =  row[0]

	print "Account with password %s created under session %s" %(passwd, sessionID)
	
	# get account creation details
	sessionDetailsSQL = "SELECT * FROM sessions WHERE id = %s" % sessionID
	cur.execute(sessionDetailsSQL)
	
	for row in cur.fetchall():
		sessionDate = row[1]
		sessionIP = row[4]

	print "[*] created: \t %s" % sessionDate
	print "[*] from: \t %s" % sessionIP

	# Session input during account creation
	sessionInputSQL = "SELECT input FROM input WHERE session = %s" % sessionID
	cur.execute(sessionInputSQL)
	for row in cur.fetchall():
		print "[input]\t %s" %row[0]


	# Later sessions with same passwd
	loginSQL = "Select session FROM auth WHERE success = 1 AND password = '%s'" % passwd
	cur.execute(loginSQL)
	for row in cur.fetchall():
		sessionID = row[0]
		sessionDetailsSQL = "SELECT * FROM sessions WHERE id = %s" % sessionID

		# Session summaries
		sessionCur = kippodb.cursor()
		sessionCur.execute(sessionDetailsSQL)
		for sessionRow in sessionCur.fetchall():
			print "[*]Date: %s from %s" % (sessionRow[1], sessionRow[4])

