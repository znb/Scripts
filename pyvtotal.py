#!/usr/bin/python

# submit files, hashes or URLs to VirusTotal
# code @ zonbi.org Matt

from optparse import OptionParser
import sys
import simplejson
import urllib
import urllib2
import hashlib

# edit this for your key
vtkey = "PUTYOURAPIKEYHERE"
                   
# submit a file (this isn't working yet)
def submit_file(sfile):
        print "<< pyVTotal v0.1a >>"
        print "Submitting file: ", sfile
        # Create hashes of your file
        print "Calculating hash: " 
        sha = hashlib.sha256(sfile).hexdigest()
        print "sha256: " , sha
        md5 = hashlib.md5(sfile).hexdigest()
        print "md5: ", md5
        # check that the hash doesn't exist already
        
        # submit the file
        print "Done."
       
# submit a hash (this is working) 
def submit_hash(shash):
        print "<< pyVTotal v0.1a >>"
        print ""
        print "Submitting hash: ", shash
        
        url = "https://www.virustotal.com/vtapi/v2/file/report"
        parameters = {"resource": shash,"apikey": vtkey}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        json = response.read()
        url_dict = simplejson.loads(json)
        resp = url_dict.get("response_code", {})
        if resp == 0:
            print "Nothing in VT database for: ", shash
            sys.exit()
        else:
            url = url_dict['permalink']    
            print "Virus Total Report: ", url
            #results = results_dict['report']
            print "<!--------- Scan Results --------!>"
            print ""
            mcafee = url_dict.get("scans", {}).get("McAfee", {}).get("result")
            print "[01] McAfee: ", mcafee
            avg = url_dict.get("scans", {}).get("AVG", {}).get("result")
            print "[02] AVG: ", avg
            clam = url_dict.get("scans", {}).get("ClamAV", {}).get("result")
            print "[03] ClamAV: ", clam
            msoft = url_dict.get("scans", {}).get("Microsoft", {}).get("result")
            print "[04] Microsoft: ", msoft
            bdefender = url_dict.get("scans", {}).get("BitDefender", {}).get("result")
            print "[05] BitDefender: ", bdefender
            symantec = url_dict.get("scans", {}).get("Symantec", {}).get("result")
            print "[06] Symantec: ", symantec
            tmicro = url_dict.get("scans", {}).get("TrendMicro", {}).get("result")
            print "[07] TrendMicro: ", tmicro
            sophos = url_dict.get("scans", {}).get("Sophos", {}).get("result")
            print "[08] Sophos: ", sophos
            ksky = url_dict.get("scans", {}).get("Kaspersky", {}).get("result")
            print "[09] Kaspersky: ", ksky
            nod = url_dict.get("scans", {}).get("NOD32", {}).get("result")
            print "[10] NOD32: ", nod
            
            print ""
            print "<!--------- Done --------!>"
        
# submit a URL (I think this is working)
def submit_url(surl):
        print "<< pyVTotal v0.1a >>"
        print ""
        print "Submitting URL: ", surl
        
        vturl = "https://www.virustotal.com/vtapi/v2/url/scan"
        parameters = {"url": surl,"apikey": vtkey}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(vturl, data)
        response = urllib2.urlopen(req)
        json = response.read()
        response_dict = simplejson.loads(json)
        url = response_dict['permalink']
        print "Virus Total Report: ", url
        scan_id = response_dict.get("scan_id", {})
        print "Scan ID: ", scan_id
        print ""
        print "Done."
        
# submit a URL scan id (this isn't working)
def scanid(scanid):
        print "<< pyVTotal v0.1a >>"
        print ""
        print "Submitting Previous Scan ID: ", scanid
        
        vturl = "https://www.virustotal.com/vtapi/v2/url/report"
        parameters = {"scan_id": scanid,"apikey": vtkey}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(vturl, data)
        response = urllib2.urlopen(req)
        json = response.read()
        print json
        #response_dict = simplejson.loads(json)
        #print "Scan ID: ", scan_id
        #print ""
        #print "Done."
        
        print ""
        print "Done."

# main menu and kick off the application
def main():
        
        p = OptionParser(usage="%prog --help", version="%prog 0.1a")
        p.add_option("--hash", 
                    action="store", 
                    type="string", 
                    dest="hash", 
                    help="Hash to submit")
        p.add_option("--file",
                     action="store",
                     type="string",
                     dest="file",
                     help="File to submit")
        p.add_option("--url",
                     action="store",
                     type="string",
                     dest="url",
                     help="URL to submit")
        p.add_option("--scanid",
                     action="store",
                     type="string",
                     dest="scan_id",
                     help="Previous Scan ID")

        options, args = p.parse_args()
        
        if len(args) >= 1:
            print "<< pyVTotal v0.1a >>"
            p.print_help()
            sys.exit()
            
        elif options.file: 
            sfile = options.file
            submit_file(sfile)
            
        elif options.hash:
            shash = options.hash
            submit_hash(shash)
            
        elif options.url:
            surl = options.url
            submit_url(surl)
            
        elif options.scan_id:
            scan_id = options.scan_id
            scanid(scan_id)
            
        else:
            print "<< pyVTotal v0.1a >>"
            p.print_help()
            sys.exit()        


if __name__ == "__main__":
        main()
