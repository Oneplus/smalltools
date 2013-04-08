#!/usr/bin/env python

import os
import sys
import random

try:
    # module has been installed
    from corpusproc.io import SegmentReader, PostagReader, ConllReader, PlainReader
    from corpusproc.io import SegmentWriter, PostagWriter, ConllWriter, PlainWriter
    from corpusproc.io import FORMATS
except:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from corpusproc.io import SegmentReader, PostagReader, ConllReader, PlainReader
    from corpusproc.io import SegmentWriter, PostagWriter, ConllWriter, PlainWriter
    from corpusproc.io import FORMATS

from optparse import OptionParser

def createObject(className, * args):
    cls = globals()[className]

    if isinstance(cls, type) and isinstance(args[0], file):
        return cls(args[0])
    else:
        raise Exception("No such class")

if __name__=="__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f", "--format",
            dest="format",
            help="use to specify format[segment,postag,plain]")

    opt_parser.add_option("-m", "--mode",
            dest="mode",
            help="use to specify mode[number,percent]")

    opt_parser.add_option("-r", "--random",
            dest="random",
            action="store_true",
            default=False,
            help="use to specify random sample")

    opt_parser.add_option("-t", "--template",
            dest="template",
            help="use to specify split template, eg. --template=\"train:7,dev:1,test:2\"")

    opt, args= opt_parser.parse_args()

    print opt.template

    def parse(item):
        ret = {}
        ret["suffix"]=item.split(":")[0]
        ret["number"]=int(item.split(":")[1])
        ret["handle"]=createObject(
                opt.format[0].upper() + opt.format[1:] + "Writer",
                open(args[0]+".%s"%ret["suffix"], "w"))
        return ret

    config = [parse(item) for item in opt.template.split(",")]

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

    inst = reader.get()
    insts = [inst]
    line_num = 0

    while inst is not None:
        line_num += 1
        insts.append(inst)
        inst = reader.get()

    if opt.random:
        insts.shuffle()

    if opt.mode == "number":
        f = 0
        for idx, c in enumerate(config):
            config[idx]["from"] = f
            config[idx]["to"] = f + c["number"]
            f += c["number"]
    elif opt.mode == "percent":
        f = 0; all = sum(c["number"] for c in config)
        for idx, c in enumerate(config):
            die = int(float(c["number"]) / all * line_num)
            config[idx]["from"] = f
            config[idx]["to"] = f + die
            f += die

    print config
    for c in config:
        for i in insts[c["from"]: c["to"]]:
            c["handle"].write(i)
