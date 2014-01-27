# Simple IMAP Test Script

from imapclient import IMAPClient
import argparse
import sys


def testserver(aserver, aport, auser, apassword):
    """Do work"""
    server = IMAPClient(aserver, aport, use_uid=True, ssl=False)
    print "Logging in"
    try:
        server.login(auser, apassword)
    except Exception: 
        print "\n *** Something has gone horribly wrong ***\n"
    else:
        print "\n Great Success !\n"
        pass

    select_info = server.select_folder('INBOX')
    print '%d messages in INBOX' % select_info['EXISTS']

    messages = server.search(['NOT DELETED'])
    print "%d messages that aren't deleted" % len(messages)

    print "\n Message Summary:"
    response = server.fetch(messages, ['FLAGS', 'RFC822.SIZE'])
    for msgid, data in response.iteritems():
        print '   ID %d: %d bytes, flags=%s' % (msgid,
        data['RFC822.SIZE'],
        data['FLAGS'])

    sys.exit("\nWe're done here")


def __main__():

    parser = argparse.ArgumentParser(description='Simple imap tester', usage='%(prog)s -s server -p port -u user -P password')
    parser.add_argument('--server', '-s', dest='server', help='server to test')
    parser.add_argument('--port', '-p', dest='port', help='port to use')
    parser.add_argument('--user', '-u', dest='user', help='username')
    parser.add_argument('--password', '-P', dest='password', help='password')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    aserver = args.server
    aport = args.port
    auser = args.user
    apassword = args.password

    if not args.server:
        sys.exit(parser.print_help())

    print ""
    print "Starting IMAP Tester"
    testserver(aserver, aport, auser, apassword)


if __name__ == '__main__':
    __main__()
