import getopt, random, sys, os
import DD


def usage():
    print """--infile= --outfile= --tempfile= --stringchunk"""

def runDD():
    global inFile, outFile, tmpFile, dontIgnore, stringchunk
    print "Delta Debugger started"
    print "Using infile=%s, outfile=%s, tempfile=%s" % (inFile, outFile, tmpFile)

    mydd = DD.PSDD(dontIgnore, tmpFile)
    # mydd.debug_test     = 1			# Enable debugging output
    # mydd.debug_dd       = 1			# Enable debugging output
    # mydd.debug_split    = 1			# Enable debugging output
    # mydd.debug_resolve  = 1			# Enable debugging output

    # mydd.cache_outcomes = 0
    # mydd.monotony = 0

    list = [(0,'')]
    f = open(inFile, 'r')
    try:
#    with open(filename,'r') as f:
        data = f.read()
        index = 1
        for c in data:
            list.append((index, c))
            index += 1
#        for line in f.readlines():
#            list.extend(line.split())
#            list.append('\n')
    finally:
        f.close()

#    f = open('pre.out', 'wt')
#    try:
#    with open('pre.out', 'wt') as f:
#        f.write(''.join([str(tup) for tup in list]))# + '\n')
#    print ' '.join(list)
#    sys.exit()
#    finally:
#        f.close()
    print "Computing the failure-inducing difference..."
#    (c, c1, c2) = mydd.dd(list)	# Invoke DD
    c = mydd.ddmin(list)
    print "The 1-minimal failure-inducing difference is", c
    #   print c1, "passes,", c2, "fails"
    c_sorted = c[:]
    c_sorted.sort()

    f = open(outFile, 'wt')
    try:
    #with open('min.out', 'wt') as f:
        for tup in c_sorted:
            f.write(tup[1])
    finally:
        f.close()
    os.remove(tmpFile)


def ParseArguments():
	global inFile, outFile, tmpFile, dontIgnore, stringchunk
        try:
            optionals, args = getopt.getopt(sys.argv[1:], "i:o:t:d:p:s", ["infile=", "outfile=", "tempfile=", "dontignore=", "prefile=", "stringchunk"])
        except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            usage()
            sys.exit(2)
        inFile = 'dd.in'
        outFile = 'min.out'
        tmpFile = '/tmp/tmp' + str(random.randint(0, 999999999)) + '.dd'
        stringchunk = False
        dontIgnore = -1

        for o, a in optionals:
            if o in ("-i", "--infile"):
                inFile = a
            elif o in ("-o", "--outfile"):
                outFile = a
            elif o in ("-t", "--tempfile"):
                tmpFile = a
            elif o in ("-d", "--dontignore"):
                dontIgnore = int(a)
            elif o in ("-s", "--stringchunk"):
                stringchunk = True
            else:
                usage()
                sys.exit()
        runDD()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

if __name__ == "__main__":
    ParseArguments()
