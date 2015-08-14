#!/usr/bin/python
# Pull DNS entries from a hosts list

import argparse
import dns.resolver
import dns.reversename
import socket


def dnsquery(ahost, adnsserver, aoutput):
    """Perform DNS queries"""
    dresolver = dns.resolver.Resolver()
    dresolver.nameservers = [adnsserver]
    fout = open(aoutput, 'a')
    try:
        ans = dresolver.query(ahost)
        for rdata in ans:
            print "[*] DNS Record found : ", 
            rhost = rdata.address
            print "Opening socket: " + rhost, 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((rhost,443))
            if result == 0:
                print " : Port open. Adding to file :)"
                fout.write(rhost + '\n')
            else:
                print " : Port closed."
            sock.close()
            
    except dns.exception.DNSException as e:
        if isinstance(e, dns.resolver.NoNameservers):
            print "[*] No name server record: %s " % ahost


def fileparse(ahost, adnsserver, afile, aoutput):
    """Pull hosts from a file"""
    print "Dumping to file: " + aoutput
    fh = open(afile, 'r')
    for line in fh:
        qhost = line.rstrip()
        dnsquery(qhost, adnsserver, aoutput)
        
    fh.close()
    print "We're done here"

def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='basic dns query system', usage='%(prog)s -f file -t <query type>')
    parser.add_argument('--file', '-f', dest='filein', help='file to pull hosts from')
    parser.add_argument('--output', '-o', dest='output', help='file to dump results to')
    parser.add_argument('--host', '-H', dest='host', help='Hostname to query')
    parser.add_argument('--server', '-s', dest='dnsserver', default='8.8.8.8', help='DNS server to query')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.filein
    ahost = args.host
    aoutput = args.output
    global adnsserver
    adnsserver = args.dnsserver

      
    if args.filein:
        fileparse(ahost, adnsserver, afile, aoutput)
    else:
        dnsquery(ahost, adnsserver, aoutput)


if __name__ == '__main__':
    __main__()
