#!/usr/bin/python
# Simple IP check script

import argparse
import sys
import dns.resolver
import dns.reversename
import whois


def check_dns(ahost, anameserver):
    """Check DNS entry for hostname"""
    dresolver = dns.resolver.Resolver()
    dresolver.nameservers = [anameserver]
    dresolver.timeout = 3
    print "DNS Resolver: " + anameserver
    ans = dresolver.query(ahost)
    try:
        for rdata in ans:
            return rdata.address
    except Exception as e:
        print "Error: %s" % e


def check_reverse(dns_check):
    """Check the reverse DNS for the IP given in DNS"""
    addr = dns.reversename.from_address(dns_check)
    reverse = dns.resolver.query(addr, "PTR")[0]
    return reverse


def check_whois(ahost):
    """Check whois for the domain"""
    domain = ahost.partition('.')[2]
    domain = whois.query(ahost)
    print "Whois information:"
    print "Registrar: " + str(domain.registrar)
    print "Creation date: " + str(domain.creation_date)
    print "Expiration date: " + str(domain.expiration_date)
    print "Name servers: " 
    for ns_servers in domain.name_servers:
        print "\t" + ns_servers
    


def run_checks(ahost, anameserver):
    """All our checks start here"""
    dns_check = check_dns(ahost, anameserver)
    print "DNS Check: " + dns_check   
    reverse_dns = check_reverse(dns_check)
    print "Reverse IP: " + str(reverse_dns)
    whois_check = check_whois(ahost)
    

def __main__():

    parser = argparse.ArgumentParser(description='Simple hostname check script')
    parser.add_argument('--host', '-H', dest='host', help='hostname to check')
    parser.add_argument('--nameserver', '-n', dest='nameserver', default='8.8.8.8', help='nameserver to check against')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    ahost = args.host
    anameserver = args.nameserver

    if not args.host:
        sys.exit(parser.print_help())

    print "Checking: " + ahost
    run_checks(ahost, anameserver)


if __name__ == '__main__':
    __main__()
