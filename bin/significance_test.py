#!/usr/bin/env python

# a script for test of statistical significance
# input of this script is the output of eval.py with
# -a configed
import sys
import random
from optparse import OptionParser, make_option

if __name__=="__main__":
    opt_list = [
            make_option("-n", "--num_iter",
                dest="num_iter", type="int", default=10000,
                help="use to specify number iteration"),
            make_option("--m1",
                dest="model1"),
            make_option("--m2",
                dest="model2")]
    opt_parser = OptionParser(option_list = opt_list)

    opts, args = opt_parser.parse_args()

    try:
        model1name = open(opts.model1, "r")
        model2name = open(opts.model2, "r")
    except:
        print >> sys.stderr, "failed to open file"
        sys.exit(1)

    recallIdx = 0;
    precisionIdx = 1;
    matchIdx = 2;
    goldIdx = 2;
    productedIdx = 4;

    def avgRecall(data):
        return float(sum([d[recallIdx] for d in data])) / sum([d[goldIdx] for d in data])

    def avgPrecision(data):
        return float(sum([d[recallIdx] for d in data])) / sum([d[precisionIdx] for d in data])

    def avgF(data):
        p = avgPrecision(data)
        r = avgRecall(data)
        f = 2*p*r / (p + r)
        return f

    m1Data = []
    m2Data = []
    for line in model1name:
        m1Data.append([int(i) for i in line.strip().split()[:3]])
    for line in model2name:
        m2Data.append([int(i) for i in line.strip().split()[:3]])

    recalls = [avgRecall(m1Data), avgRecall(m2Data)]
    precisions = [avgPrecision(m1Data), avgPrecision(m2Data)]
    fs = [avgF(m1Data), avgF(m2Data)]

    recallDiff = recalls[1] - recalls[0]
    print >> sys.stderr, "model2 recall - model1 recall = %.6f" % recallDiff

    precisionDiff = precisions[1] - precisions[0]
    print >> sys.stderr, "model2 precision - model1 precision = %.6f" % precisionDiff

    fDiff = fs[1] - fs[0]
    print >> sys.stderr, "model2 f - model1 f = %.6f" % fDiff

    print >> sys.stderr, "Doing random shuffle %d times" % opts.num_iter

    randomRecallDiff = 0
    randomPrecisionDiff = 0
    randomFDiff = 0

    for iter in xrange(opts.num_iter):
        if (iter > 0 and iter % 1000 == 0):
            print >> sys.stderr, ("Complete %d iterations" % iter)

        for i in xrange(len(m1Data)):
            shuffle = random.random()
            if shuffle > 0.5:
                m1Data[i], m2Data[i] = m2Data[i], m1Data[i]

        currRecallDiff = avgRecall(m2Data) - avgRecall(m1Data)
        if recallDiff >= 0 and currRecallDiff >= recallDiff:
            randomRecallDiff += 1
        elif recallDiff < 0 and currRecallDiff < recallDiff:
            randomRecallDiff += 1

        currPrecisionDiff = avgPrecision(m2Data) - avgPrecision(m1Data)
        if precisionDiff >= 0 and currPrecisionDiff >= precisionDiff:
            randomPrecisionDiff += 1
        elif precisionDiff < 0 and currPrecisionDiff < precisionDiff:
            randomPrecisionDiff += 1

        currFDiff = avgF(m2Data) - avgF(m1Data)
        if fDiff >= 0 and currFDiff >= fDiff:
            randomFDiff += 1
        elif fDiff < 0 and currFDiff < fDiff:
            randomFDiff += 1

    print >> sys.stderr, ("number of random recall differences equal to or greater than"
        "origin observed difference: %d" % randomRecallDiff)
    print >> sys.stderr, ("number of precision recall differences equal to or greater than"
        "origin observed difference: %d" % randomPrecisionDiff)
    print >> sys.stderr, ("number of precision f differences equal to or greater than"
        "origin observed difference: %d" % randomFDiff)

    print >> sys.stderr, "p-value for recall diff: %.8f" % (float(randomRecallDiff+1)/(opts.num_iter + 1))
    print >> sys.stderr, "p-value for precision diff: %.8f" % (float(randomPrecisionDiff+1)/(opts.num_iter + 1))
    print >> sys.stderr, "p-value for f diff: %.8f" % (float(randomFDiff+1)/(opts.num_iter + 1))

