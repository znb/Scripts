#!/usr/bin/python

# I'm lazy. I don't like manually browsing SQLite databases
# code @ zonbi.org Matt

import sys
from optparse import OptionParser
import sqlite3

def tbldump(sdb):
    conn = sqlite3.connect(sdb)
    c = conn.cursor()
    c.execute('select name from sqlite_master where type=\'table\' ORDER BY name')
    print "Tables found: "
    print "--------------------------------------"
    for table in c:
        print table[0]
    print "--------------------------------------"
    dmptbls = raw_input("Dump tables to file (y/n) ? ")
    if dmptbls == "y":
        dumptbl = raw_input("Tables to dump: ")
        fileout = raw_input("enter file name: ")
        rows = c.execute("SELECT * from %s" % dumptbl)
        if fileout == "":
            print "dumping to STDOUT"
            for row in rows:
                    print row
        else:    
            print "dumping " + dumptbl +" to:", fileout
            # I need to fix this
            # Code to dump tables to file
            for row in rows:
                print row
            

        print "all done"
        sys.exit()        
    elif dmptbls == "n":
        c.close()
        print "exiting"
        sys.exit()
    else: 
        c.close()
        print "exiting"
        sys.exit()

def main():
    p = OptionParser(usage="%prog --help", version="%prog 0.1")
    p.add_option("-f", 
                action="store", 
                type="string", 
                dest="file", 
                help="Database file to open")
    
    options, args = p.parse_args()
    
    if len(args) == 1:
        print "<< pySQLitExplore v0.1 >>"
        p.print_help()
        sys.exit()        
    else:
        print "<< pySQLitExplore v0.1 >>" 
        sdb = options.file
        print "Exploring ", sdb
        tbldump(sdb)
        
if __name__ == "__main__":
        main()