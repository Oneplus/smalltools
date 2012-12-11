#!/usr/bin/env python

import os
import sys
import random

try:
    # module has been installed
    from corpusproc.io import PlainReader, SegmentReader, PostagReader, ConllReader
    from corpusproc.io import PlainWriter, SegmentWriter, PostagWriter, ConllWriter
    from corpusproc.io import FORMATS
    from corpusproc.detect import detect
except:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from corpusproc.io import PlainReader, SegmentReader, PostagReader, ConllReader
    from corpusproc.io import PlainWriter, SegmentWriter, PostagWriter, ConllWriter
    from corpusproc.io import FORMATS
    from corpusproc.detect import detect

def createObject(className, * args):
    cls = globals()[className]

    if isinstance(cls, type) and isinstance(args[0], file):
        return cls(args[0])
    else:
        raise Exception("No such class")

from optparse import OptionParser

if __name__=="__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f",
            "--format",
            dest="format",
            default=None,
            help="use to specify input corpus format")

    opt_parser.add_option("-e",
            "--encoding",
            dest="encoding",
            default="utf8",
            help="use to specify input corpus' encoding")

    opt, args = opt_parser.parse_args()

    try:
        fp=open(args[0], "r")
    except:
        msg = "Failed to open file."
        print >> sys.stderr, msg
        exit(1)

    if opt.format is None or opt.format not in FORMATS:
        msg = "# (unknown corpus format, run auto detect corpus format)"
        print >> sys.stderr, msg
        # detect corpus type
        text=""
        line_count = 0
        for line in fp:
            text += line
            if line_count >= 1000:
                break
        opt.format = detect(text)
        msg = "# (auto detect result show corpus in [%s] format)" % opt.format
        print >> sys.stderr, msg
        fp.seek(0)

    try:
        reader = createObject(opt.format[0].upper() + opt.format[1:] + "Reader", fp)
    except:
        print >> sys.stderr, "Failed to open file"

    num_char = 0
    num_word = 0
    num_sent = 0

    inst = reader.get()
    while inst is not None:
        num_sent += 1
        num_word += len(inst)
        if opt.format == "plain":
            num_char += len(inst.raw.decode(opt.encoding))
        else:
            for form in inst.forms:
                chars = form.decode(opt.encoding)
                num_char += len(chars)

        inst = reader.get()

    print >> sys.stderr, "Number characters:  %d" % num_char
    print >> sys.stderr, "Number words:       %s" % (
            "%.2f" % num_word if num_word > 0 else "-")
    print >> sys.stderr, "Number sentences:   %d" % num_sent
    print >> sys.stderr, "Average words/sent: %s" % (
            "%.2f" % (float(num_word)/num_sent) if num_word > 0 else "-")
    print >> sys.stderr, "Average chars/sent: %s" % (float(num_char)/num_sent)
    print >> sys.stderr, "Average chars/word: %s" % (
            "%.2f" % (float(num_char)/num_word) if num_word > 0 else "-")
