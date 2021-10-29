#!/usr/bin/python
# Simple GlastopfNG database query tool
# v2 will allow you to specify the database to query

from pysqlite2 import dbapi2 as sqlite
import sys

args = sys.argv[1]

connection = sqlite.connect('sqLitedb.db')
cursor = connection.cursor()

# Show all database entries
def returnall():
        cursor.execute('SELECT * FROM log')
        for row in cursor:
                print row

# Search for a specific string
def search():
        query = sys.argv[2]
        cursor.execute("SELECT * FROM log WHERE request LIKE '%"+query+"%'")
        for row in cursor:
                print row

# Search for a specific IP address
def ipquery():
        ip = sys.argv[2]
        cursor.execute("SELECT * FROM log WHERE attacker = '"+ip+"'")
        for row in cursor:
                print row

if args == "-a":
        returnall()
elif args == "-s":
        search()
elif args == "-i":
        ipquery()

