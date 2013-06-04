#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys

if __name__=="__main__":
    try:
        fp=open(sys.argv[1], "r")
    except:
        print >> sys.stderr, "failed to open file."
        exit(1)
        
    try:
        fpo=open(sys.argv[2], "w")
    except IOError:
        print >> sys.stderr, "failed to open file."
        exit(1)

    def parse(wordstr):
        word, tag = wordstr.rsplit("_", 1)
        return word.decode("utf8"), tag
        
    def merge(word):
        return "%s_%s" % (word[0].encode("utf8"), word[1])

    for line in fp:
        words = [parse(word) for word in line.strip().split()]
        line = []
        i = 0
        while i < len(words):
            f = False
            if i + 1 < len(words):
                if ((words[i][0] + words[i+1][0] == u"。”") or
                    (words[i][0] + words[i+1][0] == u"！”") or 
                    (words[i][0] + words[i+1][0] == u"？”") or 
                    (words[i][0] + words[i+1][0] == u"；”") or
                    (words[i][0] + words[i+1][0] == u"……”") or
                    (words[i][0] + words[i+1][0] == u"？！")):
                    line.append(merge(words[i])); i += 1
                    line.append(merge(words[i])); i += 1
                    print >> fpo, " ".join(line)
                    line = []
                    f = True

            if (not f and (words[i][0] == u"。" or
                words[i][0] == u"！" or 
                words[i][0] == u"？" or 
                words[i][0] == u"；" or
                words[i][0] == u"……")):

                line.append(merge(words[i])); i += 1
                print >> fpo, " ".join(line)
                line = []
                f = True

            if not f:
                line.append(merge(words[i]))
                i += 1

        if len(line) > 0:
            print >> fpo, " ".join(line)

