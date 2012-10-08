#!/usr/bin/env python

import os
import sys
import random

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

def evaluate(pred, gold, mode="segment"):
    assert (pred.raw == gold.raw)

    gold_words = 0
    pred_words = 0
    reco_words = 0
    reco_pos   = 0

    if mode == "postag":
        assert len(pred) == len(gold)

        L = len(pred)
        for i in xrange(L):
            if pred.postags[i] == gold.postags[i]:
                reco_pos += 1

        gold_words = L
        return (reco_pos, gold_words)
    else:
        m, n = 0, 0
        gold_len, pred_len = 0, 0

        while m < len(pred) and n < len(gold):
            if pred.forms[m] == gold.forms[n]:
                reco_words += 1

                if mode == "joint":
                    if pred.postags[m] == gold.postags[n]:
                        reco_pos += 1

                gold_len += len(gold.forms[n])
                pred_len += len(pred.forms[m])

                m += 1
                n += 1

            else:
                gold_len += len(gold.forms[n])
                pred_len += len(pred.forms[m])

                m += 1
                n += 1

                while (m < len(pred)) and (n < len(gold)):
                    if (gold_len > pred_len):
                        pred_len += len(pred.forms[m])
                        m += 1
                    elif (gold_len < pred_len):
                        gold_len += len(gold.forms[n])
                        n += 1
                    else:
                        break

        pred_words += len(pred)
        gold_words += len(gold)

        if mode == "segment":
            return (reco_words, pred_words, gold_words)
        else:
            return (reco_words, reco_pos, pred_words, gold_words)

if __name__=="__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f",
            "--format",
            dest="format",
            help="use to specify format")

    opt_parser.add_option("-m",
            "--mode",
            dest="mode",
            help="use to specify evaluation mode.")

    opt_parser.add_option("-e",
            "--eval",
            dest="evalfile",
            help="use to specify eval file.")

    opt_parser.add_option("-g",
            "--gold",
            dest="goldfile",
            help="use to specify gold file.")

    opt, args = opt_parser.parse_args()

    if opt.mode not in ["segment", "postag", "joint"]:
        msg = "unknown mode [%s]" % opt.mode
        print >> sys.stderr, msg
        exit(1)

    if opt.format not in ["segment", "postag", "conll"]:
        msg = "unknown corpus format [%s]" % opt.format
        print >> sys.stderr, msg
        exit(1)

    try:
        eval_stream = createObject(opt.format[0].upper() + opt.format[1:] + "Reader", open(opt.evalfile, "r"))
    except:
        msg = "failed to open eval file [%s]" % opt.evalfile
        print >> sys.stderr, msg
        exit(1)

    try:
        gold_stream = createObject(opt.format[0].upper() + opt.format[1:] + "Reader", open(opt.goldfile, "r"))
    except:
        msg = "failed to open gold file [%s]" % opt.goldfile
        print >> sys.stderr, msg
        exit(1)

    pred_inst = eval_stream.get()
    gold_inst = gold_stream.get()

    results = [0] * 4
    while pred_inst is not None and gold_inst is not None:
        if opt.mode == "segment":
            num_recall, num_pred, num_gold = evaluate(pred_inst, gold_inst, opt.mode)
            results[0] += num_recall
            results[1] += num_pred
            results[2] += num_gold

        elif opt.mode == "postag":
            num_recall, num_gold = evaluate(pred_inst, gold_inst, opt.mode)
            results[0] += num_recall
            results[1] += num_gold

        else:
            num_recall, num_recall_pos, num_pred, num_gold = evaluate(pred_inst, gold_inst, opt.mode)
            results[0] += num_recall
            results[1] += num_recall_pos
            results[2] += num_pred
            results[3] += num_gold

        pred_inst = eval_stream.get()
        gold_inst = gold_stream.get()

    if pred_inst is None and gold_inst is not None:
        msg = "gold stream not end"
        print >> sys.stderr, msg

    if pred_inst is not None and gold_inst is None:
        msg = "predict stream not end"
        print >> sys.stderr, msg

    if opt.mode == "segment":
        p = float(results[0])/results[1]*100
        r = float(results[0])/results[2]*100
        f = p*r*2/(p+r)
        print "p=%.8f%% r=%.8f%% f=%.8f%%" % (p, r, f)

    elif opt.mode == "postag":
        p = float(results[0])/results[1]*100
        print "p=%.8f%%" % p

    else:
        p = float(results[0])/results[2]*100
        r = float(results[0])/results[3]*100
        f = p*r*2/(p+r)
        pp = float(results[1])/results[2]*100
        pr = float(results[1])/results[3]*100
        pf = pp*pr*2/(pp+pr)
        print "seg: p=%.8f%% r=%.8f%% f=%.8f%%" % (p, r, f)
        print "pos: p=%.8f%% r=%.8f%% f=%.8f%%" % (p, r, f)

