#!/usr/bin/env python

import os
import sys
import random

try:
    # module has been installed
    from smalltools.io import SegmentReader, PostagReader, ConllReader, PlainReader
    from smalltools.io import SegmentWriter, PostagWriter, ConllWriter, PlainWriter
    from smalltools.io import FORMATS
except:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from smalltools.io import SegmentReader, PostagReader, ConllReader, PlainReader
    from smalltools.io import SegmentWriter, PostagWriter, ConllWriter, PlainWriter
    from smalltools.io import FORMATS

from optparse import OptionParser

def sample(reader, writer, index):
    index.sort()

    idx = 0
    num = 0

    inst = reader.get()
    while inst is not None and len(index) > 0:
        if idx == index[0]:
            writer.write(inst)
            index = index[1:]
            num += 1

        idx += 1
        inst = reader.get()

    return num

def createObject(className, * args):
    cls = globals()[className]

    if isinstance(cls, type) and isinstance(args[0], file):
        return cls(args[0])
    else:
        raise Exception("No such class")

if __name__=="__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f",
            "--format",
            dest="format",
            help="use to specify format[segment,postag,plain]")

    opt_parser.add_option("-m",
            "--mode",
            dest="mode",
            default="num",
            help="use to specify mode [number,percent]")

    opt_parser.add_option("-n",
            "--number",
            type="int",
            default=1,
            help="use to specify sample size")

    opt_parser.add_option("-p",
            "--percent",
            dest="percent",
            type="float",
            default=0.618,
            help="use to specify percent")

    opt, args= opt_parser.parse_args()

    if opt.mode not in ["percent", "number"]:
        msg = "unknown mode [%s]" % opt.mode
        print >> sys.stderr, msg
        exit(1)

    if opt.format not in FORMATS:
        msg = "unknown corpus format [%s]" % opt.format
        print >> sys.stderr, msg
        exit(1)

    if len(args) < 1:
        msg = "input file should be specified."
        print >> sys.stderr, msg
        exit(1)

    try:
        reader = createObject(opt.format[0].upper() + opt.format[1:] + "Reader", open(args[0]))
    except:
        msg = "failed to open file [%s]" % args[0]
        print >> sys.stderr, msg
        exit(1)

    writer = createObject(opt.format[0].upper() + opt.format[1:] + "Writer", sys.stdout)

    if opt.mode == "number":
        inst = reader.get()
        line_num = 0

        while inst is not None:
            line_num += 1
            inst = reader.get()

        sample_index = random.sample(xrange(line_num), opt.number)

    elif opt.mode == "percent":

        if opt.percent < 0.0 or opt.percent > 1.0:
            msg = "percentage should be set between (0.0, 1.0)"
            print >> sys.stderr, msg
            exit(1)

        line_num = 0
        inst = reader.get()

        while inst is not None:
            line_num += 1
            inst = reader.get()

        sample_index_size = int(round(line_num * opt.percent))
        sample_index = random.sample(xrange(line_num), sample_index_size)


    reader.seek(0, 0)
    sample(reader, writer, sample_index)
