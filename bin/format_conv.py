#!/usr/bin/env python

import os
import sys

try:
    # module has been installed
    from corpusproc.io import SegmentReader, PostagReader, ConllReader
    from corpusproc.io import SegmentWriter, PostagWriter, ConllWriter
except:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from corpusproc.io import SegmentReader, PostagReader, ConllReader
    from corpusproc.io import SegmentWriter, PostagWriter, ConllWriter

from optparse import OptionParser

def createObject(className, * args):
    cls = globals()[className]

    if isinstance(cls, type) and isinstance(args[0], file):
        return cls(args[0])
    else:
        raise Exception("No such class")

if __name__=="__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f",
            "--from",
            dest="src",
            help="use to specify from corpus format")
    opt_parser.add_option("-t",
            "--to",
            dest="dst",
            help="use to specify to corpus format")

    opt, args = opt_parser.parse_args()

    if opt.src is None:
        msg = "source corpus format is not specified."
        print >> sys.stderr, msg
        exit(1)

    if opt.dst is None:
        msg = "destination corpus format should be specified"
        print >> sys.stderr, msg
        exit(1)

    if opt.src not in ["segment", "postag", "conll"]:
        msg = "unknown source corpus format [%s]" % opt.src
        print >> sys.stderr, msg
        exit(1)

    if opt.dst not in ["segment", "postag", "conll"]:
        msg = "unknown destination corpus format [%s]" % opt.dst
        print >> sys.stderr, msg
        exit(1)

    if len(args) < 1:
        msg = "input file should be specified."
        print >> sys.stderr, msg
        exit(1)

    try:
        reader = createObject(opt.src[0].upper() + opt.src[1:] + "Reader", open(args[0]))
    except:
        msg = "failed to open file [%s]" % args[0]
        print >> sys.stderr, msg
        exit(1)

    writer = createObject(opt.dst[0].upper() + opt.dst[1:] + "Writer", sys.stdout)

    inst = reader.get()

    while inst is not None:
        writer.write(inst)
        inst = reader.get()

