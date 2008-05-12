#!/usr/bin/python
from __future__ import with_statement
from BeautifulSoup import BeautifulSoup
import urllib2
import md5
from subprocess import *
from threading import Timer
import commands
import re
import os, sys
import string
import random
import getopt

cmd = './pstotext-linux-x86'
timeout = 5
found = [1,3,5,6,7,9,10,11,12,13,14,15,16,17,18,19]
chunkSize = 100
start = 0
end = 20
offset = 0 # scraper will start at the URL immediately after
#the one indexed by offset ([1,100] indexing)

outFile = ''
fileType = ''

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080416 Fedora/2.0.0.14-1.fc8 Firefox/2.0.0.14')]

reg = re.compile('BUG ([0-9]+) TRIGGERED')

def fetchHref(href):
    global opener, tmpFile, outFile, searchTerms, fileType, found, start, end, chunkSize, offset, cmd

    print href
    with open ( outFile,'at') as f:
        if len(found) == 20:
            f.write('Found all 20 bugs')
            sys.exit()
        f.write(href)
    try:
        usock = opener.open(href)
        url = usock.geturl()
        postscript = usock.read()
        usock.close()
    except IOError, error:
        with open(outFile,'a') as f:
            f.write(' ERROR ')
            if hasattr(error, 'code'):
                f.write(str(error.code))
            f.write('\n')
        return

    md = md5.new(postscript)
    with open(outFile,'a') as f:
        f.write(' ' + md.hexdigest())
    with open(tmpFile, 'wbt') as tmpf:
        tmpf.write(postscript)

    foundstr = str(found).strip('][').replace(' ', '')
    cmdstr =  '%s -ignore %s %s' % (cmd, foundstr, tmpFile)
    print cmdstr
    proc = Popen(cmdstr, shell=True, stderr=PIPE)
#    timeTest(timeout, proc)
#        print 'Input filehandle=' + str(proc.stdin)

#    try:
#        proc.stdin.write(postscript)
#    except IOError:
#        pass

    errorcode = -1
    try:
        line = proc.stderr.readline()
        print 'Output is ' + line
        m = reg.match(line)
        if m:
            errorcode = int(m.group(1))
    except IOError:
        pass
    finally:
        proc.stderr.close()

    proc.wait()
    if -1 != errorcode and errorcode not in found:
        found.append(errorcode)
    print 'Returncode=' + str(proc.returncode)


#        MonitorForkedProcess(proc, opts)
    with open(outFile, 'a') as f:
        f.write(' %d %d\n' % (proc.returncode, errorcode))
    return

def killProc(pid):
    returnCode, output = commands.getstatusoutput('kill ' + str(pid))
    return

def timeTest(time, proc):
    timer = Timer(time, killProc, (proc.pid,))
    timer.start()
    proc.wait()
    timer.cancel()

def ParseArguments():
	global inFile, outFile, tmpFile, dontIgnore, searchTerms, \
	fileType, repeat \
               , found, start, end, chunkSize, offset, cmd
        try:
            optionals, args = getopt.getopt(sys.argv[1:], "i:o:t:d:p:s:f:rh", ["infile=", "outfile=", "tempfile=", "dontignore=", "prefile=", "search=", "filetype=", "repeat", "help"])
        except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            usage()
            sys.exit(2)
        inFile = 'dd.in'
        outFile = 'urls.txt'
        tmpFile = '/tmp/tmp' + str(random.randint(0, 999999999)) + '.ps'
        stringchunk = False
        dontIgnore = -1
        repeat = False
        searchTerms = ''

        for o, a in optionals:
            if o in ("-i", "--infile"):
                inFile = a
            elif o in ("-o", "--outfile"):
                outFile = a
            elif o in ("-t", "--tempfile"):
                tmpFile = a
            elif o in ("-d", "--dontignore"):
                dontIgnore = int(a)
            elif o in ("-s", "--search"):
                searchTerms = a
	    elif o in ("-f", "--filetype"):
		fileType = a
            elif o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-r", "--repeat"):
                repeat = True
            else:
                usage()
                sys.exit()
        if searchTerms == '':
            print 'Search terms must be given'
            sys.exit()
            
        for i in xrange(start, end): #(9, 100): #00000):
            url = 'http://www.google.com/search?q=%s+filetype:%s&num=%d&hl=en&lr=&as_qdr=all&ie=UTF-8&start=%d&sa=N'\
                  % (searchTerms, fileType, chunkSize, i * chunkSize)
#    url =  'http://www.google.com/search?q=+filetype:ps+.ps&num=%d&hl=en&lr=&as_qdr=all&start=%d&sa=N' % (chunkSize, i * chunkSize)
            print url

            usock = opener.open(url)
            url = usock.geturl()
            data = usock.read()
            usock.close()

            soup = BeautifulSoup(data)
    

            hrefs = []
            for anchor in soup.fetch('a', {'class' : 'l'}):
                hrefs.append(anchor['href'])

            count = 0
            for href in hrefs:
                count += 1
                if offset > 0:
                    offset -= 1
                    print 'Skipping ' + href
                    continue
                fetchHref(href)
            print 'Finished iteration #' + str(i)
            if count < chunkSize:
                with open(outFile, 'at') as f:
                    f.write('Search results exhausted\n')
                break
            #print soup.prettify()
        os.remove(tmpFile)

if __name__ == "__main__":
    ParseArguments()

#fetchHref('http://www.cs.berkeley.edu/~christos/ir.ps')
#fetchHref('http://www.cs.vu.nl/boilerplate/slides/slides.ps') # creates IOError
#fetchHref('http://www.nhn.ou.edu/~milton/papers/kmparis.ps?ref=ARKADASBUL.NET') # ?? no error
