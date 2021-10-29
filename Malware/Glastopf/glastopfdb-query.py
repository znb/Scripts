#!/usr/bin/python
# Simple Glastopf database query tool

from pysqlite2 import dbapi2 as sqlite
import sys
import argparse


def returnall(adatabase):
    """Dump all entries in our database"""
    print "Connecting to database"
    connection = sqlite.connect(adatabase)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM events')
    for row in cursor:
        print "\nDate: %s" % row[1]
        print "Attack ID: %s" % row[0]
        print "Attacker: %s" % row[2]
        print "Request: %s" % row[3]
        print "\n*** Raw Request ***\n%s" % row[4]
        print "-" * 80
    connection.close()


def search(adatabase, aid):
    """Search for a specific attack ID"""
    print "Connecting to database"
    print "Returning info for attack ID: " + aid
    connection = sqlite.connect(adatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE id = '"+aid+"'")
    for row in cursor:
            print "\nDate: %s" % row[1]
            print "Attacker: %s" % row[2]
            print "Request: %s" % row[3]
            print "\n*** Raw Request ***\n%s" % row[4]
            print "-" * 80
    connection.close()


def ipquery(adatabase, asource):
    """Search for a specific IP address in our attack list"""
    print "Connecting to database"
    print "Returning info for attacker: " + asource
    connection = sqlite.connect(adatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE source LIKE '%"+asource+"%'")
    for row in cursor:
            print "\nDate: %s" % row[1]
            print "Attacker: %s" % row[2]
            print "Request: %s" % row[3]
            print "\n*** Raw Request *** \n%s" % row[4]
            print "-" * 80
    connection.close()


def listattackers(adatabase):
    """Print list of all attackers and their attack IDs"""
    print "Connecting to database"
    print "Attacker with total requests and related attack IDs\n"
    connection = sqlite.connect(adatabase)
    attackers = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    for row in cursor:
            w = row[2]
            x = w.split(':')[0]
            attackers.append(x)
    newattackers = sorted(set(attackers))
    for attacker in newattackers:
        ids = connection.cursor()
        ids.execute("SELECT * from events where source like '"+attacker+"%';")
        attackid = []
        for id in ids:
            x =id[0]
            attackid.append(x)
        cursor.execute("SELECT source, COUNT(*) from events where source like '"+attacker+"%';")
        for row in cursor:
            count = row[1]      
        print attacker + ": " + str(count),
        print attackid
    connection.close()


def summaryreport(adatabase):
    """Print a simple summary report"""
    print "Summary report \n"
    connection = sqlite.connect(adatabase)
    attackers = []
    cursor = connection.cursor()
    cursor.execute("SELECT source, COUNT(*) from events;")
    for row in cursor:
        print "Total events: %s" % row[1]
    connection.close()


def attacksummary(adatabase):
    """Print a simple summary of all attacks"""
    print "Attack Summary report \n"
    connection = sqlite.connect(adatabase)
    attackers = []
    cursor = connection.cursor()
    cursor.execute("SELECT * from events;")
    for row in cursor:
        print "[%s] %s" % (row[0], row[3])
    connection.close()


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Basic Glastopf Database Query Tool')
    parser.add_argument('--database', '-d', dest='database', default='glastopf.db', help='Database to query')
    parser.add_argument('--all', '-a', dest='all', action="store_true", help='Return all queries')
    parser.add_argument('--id', '-i', dest='id', help='Search for a specific attack ID')
    parser.add_argument('--source', '-s', dest='source', help='Search for a specific attacker')
    parser.add_argument('--list', '-l', dest='list', action="store_true", help='List all the attackers in database')
    parser.add_argument('--summary', '-S', dest='summary', action="store_true", help='Quick summary report')
    parser.add_argument('--attacks', '-A', dest='attacks', action="store_true", help='Just list the attacks in database')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    adatabase = args.database
    aid = args.id
    asource = args.source
    alist = args.list
    asummary = args.summary
    aattacks = args.attacks
    aall = args.all

    if not args.database:
            sys.exit(parser.print_help())

    if args.all:
            returnall(adatabase)
    if args.id:
        search(adatabase, aid)
    if args.source:
        ipquery(adatabase, asource)
    if args.list:
        listattackers(adatabase)
    if args.summary:
        summaryreport(adatabase)
    if args.attacks:
        attacksummary(adatabase)


if __name__ == '__main__':
        __main__()
