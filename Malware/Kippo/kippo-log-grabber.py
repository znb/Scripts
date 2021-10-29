#!/usr/bin/python
# Log into our honeypot and run report script

import paramiko
import argparse
import sys


def sshconnect(ahost, aport, afile, auser, akey):
    """Connect to our ssh server"""
    command = "/usr/local/bin/kippo-report.sh " + afile
    print "Connecting to : " + ahost
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(ahost, port=aport, username=auser, key_filename=akey)
        stdin, stdout, stderr = client.exec_command(command)
        report = stdout.read()
        client.close()
    except:
        print "Something has gone wrong"
	sys.exit()

    print_report = raw_input("Print report to screen ? Y/N ")
    if print_report == "y":
        print report
    else:
        pass

    save_report = raw_input("Save report to file ? Y/N ")
    if save_report == "y":
        fout = open('kippo-report.txt', 'w')
        print "Saving report"
        for line in report:
                        fout.write(line)
        fout.close()

    print "Report saved: kippo-report.txt"
    print "We're done here."


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Kippo log file grabber')
    parser.add_argument('--file', '-f', dest='file', help='Log file to parse')
    parser.add_argument('--host', '-H', dest='host', help='Host to connect to')
    parser.add_argument('--port', '-p', dest='port', default='22', help='Port to connect on')
    parser.add_argument('--user', '-u', dest='user', help='Username to use')
    parser.add_argument('--password', '-P', dest='password', help='Password to use')
    parser.add_argument('--key', '-k', dest='key', help='SSH key file to use')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    afile = args.file
    ahost = args.host
    aport = int(args.port)
    auser = args.user
    apassword = args.password
    akey = args.key

    if args.key:
        sshconnect(ahost, aport, afile, auser, akey)
    elif args.password:
        print "You should be using keys"
        sys.exit()
    else:
        sys.exit(parser.print_help())


if __name__ == '__main__':
    __main__()

