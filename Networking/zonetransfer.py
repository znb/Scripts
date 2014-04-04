#!/usr/bin/python
# Zone transfer test script 

import argparse
import sys
import dns.resolver
import dns.zone


def get_ns_records(adomain, aserver):
    """Pull NS records for our domain"""
    print "> Pulling NS records for: " + adomain
    dresolver = dns.resolver.Resolver()
    dresolver.nameservers = [aserver]
    ans = dresolver.query(adomain, 'ns')
    ns_list = []            
    try:
        for rdata in ans:
            ns_list.append(rdata)
    except Exception as e:
        print "Error: %s" % e

    return ns_list


def zone_transfer(adomain, aserver, aquiet):
    """Perform zone transfers against our name servers"""
    ns_list = get_ns_records(adomain, aserver)
    for server in ns_list:
        print "> Testing: " + str(server), 
        try: 
            z = dns.zone.from_xfr(dns.query.xfr(str(server), adomain))
            names = z.nodes.keys()
            names.sort()
            if aquiet == True:
                print "[WARNING] AXFR is allowed"
            else:
                for n in names:
                    print z[n].to_text(n)
        except Exception as e:
            msg = "AXFR not allowed (probably)"
            print "Error: %s %s" % (e, msg)

    print ""


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Check name servers for zone transfers')
    parser.add_argument('--domain', '-d', dest='domain', help='domain to check')
    parser.add_argument('--server', '-s', dest='dnsserver', default='8.8.8.8', help='DNS server to query')
    parser.add_argument('--quiet', '-q', dest='quiet', action="store_true", help='Test but dont dump')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    adomain = args.domain
    aserver = args.dnsserver
    aquiet = args.quiet

    if not args.domain:
        sys.exit(parser.print_help())
    if aquiet:
        aquiet = True

    print "Zone transfer of doom v1..."
    zone_transfer(adomain, aserver, aquiet)


if __name__ == '__main__':
    __main__()
