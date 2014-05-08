#!/usr/bin/env python
import sys
import os
from optparse import OptionParser

try:
    from smalltools.utils   import str_sbc2dbc, fast_str_sbc2dbc
    from smalltools.utils   import sbcdbc
except ImportError:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)
    from smalltools.utils   import str_sbc2dbc, fast_str_sbc2dbc
    from smalltools.utils   import sbcdbc


if __name__=="__main__":
    usage = "Use to convert single byte character to double byte character"
    optparser = OptionParser(usage)
    optparser.add_option("-f", dest="filename", help="use to specify filename")
    optparser.add_option("-e", dest="encoding", default="utf-8", help="use to specify encoding")
    optparser.add_option("-d", dest="conv_digit", default=False, action="store_true",
            help="use to specify convert digit")
    optparser.add_option("-p", dest="conv_punc", default=False, action="store_true",
            help="use to specify convert punctation")
    optparser.add_option("-f", dest="conv_letter", default=False, action="store_true",
            help="use to specify convert english letter")
    optparser.add_option("-x", dest="fast", default=False, action="store_true",
            help="use to specify fast handle")
    opts, args = optparser.parse_args()
    try:
        fp=open(opts.filename, "r")
    except:
        print >> sys.stderr, "Failed to open file %s, use stdin instead" % str(opts.filename)
        fp=sys.stdin

    flags = 0
    if opts.conv_digit:
        flags |= sbcdbc.CONV_DIGIT
    if opts.conv_letter:
        flags |= sbcdbc.CONV_LETTER
    if opts.conv_punc:
        flags |= sbcdbc.CONV_PUNC

    if opts.fast:
        for line in fp:
            print fast_str_sbc2dbc(line.strip(), flags, opts.encoding).encode(opts.encoding)
    else:
        for line in fp:
            print str_sbc2dbc(line.strip(), opts.encoding).encode(opts.encoding)
