#!/usr/bin/python
# Simple subdomain search tool
# Usage: ./subdomainquery.py -S 8.8.8.8 -s blog -f /tmp/domain_input.txt -o /tmp/output.txt

import argparse
import sys
import dns.resolver
import dns.reversename


def subdomain_query(asubdomain, adomain, afile, adnsserver, aoutput):
    """Query a domain list for subdomains"""
    print '[*] Looking for "' + asubdomain + '" in our domain list\n'
    fh = open(afile, 'r')
    fo = open(aoutput, 'a')
    for domain in fh:
        querydomain = str(asubdomain) + "." + str(domain)
        query = dnsquery(querydomain, adnsserver)
        fo.write(querydomain.rstrip() + ": " + str(query) + "\n")
        print querydomain.rstrip() + ": " + str(query)
    fh.close()
    print "\n[*] Output to: " + aoutput
    fo.close()
    print "[*] We're done here."

def dnsquery(querydomain, adnsserver):
    """Perform DNS queries"""
    dresolver = dns.resolver.Resolver()
    dresolver.nameservers = [adnsserver]
    try: 
        ans = dresolver.query(querydomain.rstrip(), 'a')
        try:
            for rdata in ans:
                return rdata.address
        except Exception as e:
            print "Error: %s" % e
    except dns.exception.DNSException as e:
        if isinstance(e, dns.resolver.NoNameservers):
            print "[*] No name server record: %s " % querydomain


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Search for a certain subdomain', usage='%(prog)s -f file -t <query type>')
    parser.add_argument('--file', '-f', dest='filein', help='file to pull hosts from')
    parser.add_argument('--domain', '-d', dest='domain', help='domain to query')
    parser.add_argument('--subdomain', '-s', dest='subdomain', help='Use this subdomain for mass query')
    parser.add_argument('--server', '-S', dest='dnsserver', default='8.8.8.8', help='DNS server to query')
    parser.add_argument('--output', '-o', dest='output', help='file to dump results to')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.filein
    adomain = args.domain
    asubdomain = args.subdomain
    aoutput = args.output 
    global adnsserver
    adnsserver = args.dnsserver

    if not args.subdomain:
        sys.exit(parser.print_help())
    
    if args.subdomain:
        subdomain_query(asubdomain, adomain, afile, adnsserver, aoutput)
        

if __name__ == '__main__':
    __main__()

