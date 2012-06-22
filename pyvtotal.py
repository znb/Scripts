#!/usr/bin/python

# submit files, hashes or URLs to VirusTotal
# code @ zonbi.org Matt

from optparse import OptionParser
import sys
import simplejson
import urllib
import urllib2
import hashlib
import httplib
import mimetypes

# edit this for your key
vtkey = "PUTYOURAPIKEYHERE"                
                   
# Took this code from http://code.activestate.com/recipes/146306/
def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                   
                   
# submit a file (this isn't working)  
# [1] check if the hash of the file exist in VT
# [2] if there's a match offer to print report
# [3] if not offer to submit the file to VT
def submit_file(sfile):
        print "<< pyVTotal v0.1a >>"
        print "Submitting file: ", sfile
        # Create hashes of your file
        md5file = open(sfile, 'rb')
        data = md5file.read()
        md5file.close()
        md5sum = hashlib.md5(data).hexdigest()
        print "MD5: ", md5sum
        # check that the hash doesn't exist already
        vturl = "https://www.virustotal.com/vtapi/v2/file/report"
        parameters = {"resource": md5sum,"apikey": vtkey}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(vturl, data)
        response = urllib2.urlopen(req)
        json = response.read()
        url_dict = simplejson.loads(json)
        resp = url_dict.get("response_code", {})
        
        # no match / response from VT
        if resp == 0:
            print "No matches in VT database for: ", md5sum
            answer = raw_input("Submit to VT (Y/N)? ")
            if answer == "y":
                print "Submitting file"
                host = "www.virustotal.com"
                selector = "https://www.virustotal.com/vtapi/v2/file/scan"
                fields = [("apikey", vtkey)]
                file_to_send = open(sfile, "rb").read()
                files = [("file", sfile, file_to_send)]
                json = post_multipart(host, selector, fields, files)
                # This isn't working
                json = response.read()
                print json
                #url_dict = simplejson.loads(json)
                #url = url_dict['permalink']
                #srvrsp = url_dict.get("verbose_msg", {})
                #print "Server Response: ", srvrsp
                #print "Virus Total Report: ", url
                #scanid = url_dict.get("sha256", {})
                #print "Scan ID: ", scanid
                print "Done"
                sys.exit()
                
            elif answer == "n":
                print "Exiting."
                sys.exit()
        # there's a match in the VT database
        else:
            print "File exists on VT"
            answer = raw_input("Print Report (Y/N)? ")
            if answer == "y":
                url = url_dict['permalink']    
                print "Virus Total Report: ", url
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
                sys.exit()
            elif answer == "n":
                print "Exiting."
                sys.exit()
        
       
# submit a hash (this is working) 
def submit_hash(shash):
        print "<< pyVTotal v0.1a >>"
        print ""
        print "Submitting hash: ", shash
        
        vturl = "https://www.virustotal.com/vtapi/v2/file/report"
        parameters = {"resource": shash,"apikey": vtkey}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(vturl, data)
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
        
# submit a URL (this isn't working yet)
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
        
# submit a URL scan id (this isn't working yet)
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
        print json # this is just for debugging
        # FIX FROM HERE DOWN
        #response_dict = simplejson.loads(json)
        #print "Scan ID: ", scan_id
        print ""
        print "Done."

# main menu and kick off the application
def main():
        
        p = OptionParser(usage="%prog --help", version="%prog 0.1a")
        p.add_option("--hash", 
                    action="store", 
                    type="string", 
                    dest="hash", 
                    help="Submit a Hash")
        p.add_option("--file",
                     action="store",
                     type="string",
                     dest="file",
                     help="Submit a File")
        p.add_option("--url",
                     action="store",
                     type="string",
                     dest="url",
                     help="Submit a URL")
        p.add_option("--scanid",
                     action="store",
                     type="string",
                     dest="scan_id",
                     help="Previous URL Scan")

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
