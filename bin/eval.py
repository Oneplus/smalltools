#!/usr/bin/env python

import os
import sys
import random

SUPPORTED_MODES = set([
        "segment",
        "postag",
        "joint-segment-postag",
        "depparsing",])

try:
    # module has been installed
    from smalltools.io      import SegmentReader, PostagReader, Conlleader
    from smalltools.io      import SegmentWriter, PostagWriter, ConllWriter
    from smalltools.io      import CONV_FORMATS
    from smalltools.lang    import Chinese, English, Danish
except ImportError:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from smalltools.io      import SegmentReader, PostagReader, ConllReader
    from smalltools.io      import SegmentWriter, PostagWriter, ConllWriter
    from smalltools.io      import CONV_FORMATS
    from smalltools.lang    import Chinese, English, Danish

def createObject(className, * args):
    cls = globals()[className]

    if isinstance(cls, type) and isinstance(args[0], file):
        return cls(args[0])
    else:
        raise Exception("No such class")

class Evaluator(object):
    PATTERN = "__uninitialized__"
    # the evaluator base class
    def evaluate(self, pred, gold):
        pass

    def report(self, results):
        pass

class POSTagEvaluator(Evaluator):
    # the postag evaluator
    PATTERN = "%d\t%d\t%.8f%%"

    def evaluate(self, pred, gold):
        assert len(pred) == len(gold)
        L = len(pred)
        reco_pos = len([i for i in range(L) if pred.postags[i] == gold.postags[i]])
        gold_words = L
        return (reco_pos, gold_words)

    def report(self, result):
        p = float(results[0])/results[1]*100
        print self.PATTERN % (results[0], results[1], p)


class SegmentEvaluator(Evaluator):
    PATTERN = "%d\t%d\t%d\t%.8f%%\t%.8f%%\t%.8f%%"
    # the segment evaluator
    def evaluate(self, pred, gold):
        m, n = 0, 0
        gold_len, pred_len = 0, 0
        reco_words, reco_pos = 0, 0
        pred_words, gold_words = len(pred), len(gold)

        while m < len(pred) and n < len(gold):
            if pred.forms[m] == gold.forms[n]:
                reco_words += 1
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
        return (reco_words, pred_words, gold_words)

    def report(self, results):
        p = float(results[0])/results[1]*100
        r = float(results[0])/results[2]*100
        try:
            f = p*r*2/(p+r)
            print self.PATTERN % (results[0], results[1], results[2], p, r, f)
        except:
            print self.PATTERN % (results[0], results[1], results[2], 0., 0., 0.)


class JointSegmentPostagEvaluator(Evaluator):
    # the joint segment postag evaluator
    PATTERN = "%d\t%d\%d\t%d\t%.8f%%\t%.8f%%\t%.8f%%\t%.8f%%\t%.8f%%\t%.8f%%"
    def evaluate(self, pred, gold):
        m, n = 0, 0
        gold_len, pred_len = 0, 0
        reco_words, reco_pos = 0, 0
        pred_words, gold_words = len(pred), len(gold)

        while m < len(pred) and n < len(gold):
            if pred.forms[m] == gold.forms[n]:
                reco_words += 1
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
        return (reco_words, reco_pos, pred_words, gold_words)

    def report(self, results):
        p = float(results[0])/results[2]*100
        r = float(results[0])/results[3]*100
        f = p*r*2/(p+r)
        pp = float(results[1])/results[2]*100
        pr = float(results[1])/results[3]*100
        pf = pp*pr*2/(pp+pr)
        print self.PATTERN % (results[0], results[1], results[2], results[3], 
                p, r, f, pp, pr, pf)

class DepparsingEvaluator(Evaluator):
    PATTERN = "UAS: %.4f ( %d / %d ) LAS: %.4f ( %d / %d )"

    def evaluate(self, pred, gold, lang = Chinese):
        assert len(pred) == len(gold)
        L = len(pred)
        correct_heads, correct_deprels = 0, 0
        for i in xrange(L):
            assert pred.postags[i] == gold.postags[i]
            if pred.postags[i] in lang.PNCT_POSTAGS:
                continue
            if pred.heads[i] == gold.heads[i]:
                correct_heads += 1
                if pred.deprels[i] == gold.deprels[i]:
                    correct_deprels += 1
        return (correct_heads, correct_deprels, len(pred))

    def report(self, results):
        uas = float(results[0]) / results[2]
        las = float(results[1]) / results[2]
        print self.PATTERN % (uas, results[0], results[2],
                las, results[1], results[2])

def build_evaluator(mode):
    if mode == "segment":
        evaluator = SegmentEvaluator()
    elif mode == "postag":
        evaluator = PostagEvaluator()
    elif mode == "joint-segment-postag":
        evaluator = JointSegmentPostagEvaluator()
    elif mode == "depparsing":
        evaluator = DepparsingEvaluator()
    else:
        raise Exception("unknown mode %s" % mode)
    return evaluator

if __name__=="__main__":
    from optparse import OptionParser

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

    opt_parser.add_option("-a",
            "--all",
            dest="all",
            action="store_true",
            default=False,
            help="use to specify detail handle.")
    opt_parser.add_option("-l",
            "--lang",
            dest="lang",
            help="use to specify language.")
    opt, args = opt_parser.parse_args()

    if opt.mode not in SUPPORTED_MODES:
        msg = "mode [%s] is not supported" % opt.mode
        print >> sys.stderr, msg
        exit(1)

    evaluator = build_evaluator(opt.mode)

    if opt.format not in CONV_FORMATS:
        msg = "unknown corpus format [%s]" % opt.format
        print >> sys.stderr, msg
        exit(1)

    try:
        eval_stream = createObject(
                opt.format[0].upper() + opt.format[1:] + "Reader",
                open(opt.evalfile, "r"))
    except:
        msg = "failed to open eval file [%s]" % opt.evalfile
        print >> sys.stderr, msg
        exit(1)

    try:
        gold_stream = createObject(
                opt.format[0].upper() + opt.format[1:] + "Reader",
                open(opt.goldfile, "r"))
    except:
        msg = "failed to open gold file [%s]" % opt.goldfile
        print >> sys.stderr, msg
        exit(1)

    pred_inst = eval_stream.get()
    gold_inst = gold_stream.get()

    results = [0] * 4
    num = 0
    while pred_inst is not None and gold_inst is not None:
        num += 1
        try:
            result = evaluator.evaluate(
                    pred_inst,
                    gold_inst)
        except Exception:
            print >> sys.stderr, "instance miss match at %d" % num

        if opt.all:
            evaluator.report(result)

        L = len(result)
        for i in xrange(L):
            results[i] += result[i]

        pred_inst = eval_stream.get()
        gold_inst = gold_stream.get()

    if pred_inst is None and gold_inst is not None:
        msg = "gold stream not end"
        print >> sys.stderr, msg

    if pred_inst is not None and gold_inst is None:
        msg = "predict stream not end"
        print >> sys.stderr, msg

    evaluator.report(results)
