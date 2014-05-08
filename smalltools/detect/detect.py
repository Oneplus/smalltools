# -*- coding: utf8 -*-
#!/usr/bin/env python
from random import sample

def _argmax(dict):
    max_argc, max_argv = None, None
    for key in dict:
        if max_argv == None or max_argv < dict[key]:
            max_argv = dict[key]
            max_argc = key

    return max_argc

def detect(corpus):
    '''
    Detect the potential format of the input corpus.

    Args:
        corpus (str): The input corpus.
    Return:
        str: The potential format of the input corpus.
    '''
    vote_box = {
            "plain":        0,
            "segment":      0,
            "postag":       0,
            "conll":        0,
            "unknown":      0};

    blocks = corpus.strip().split("\n\n")

    if len(blocks) > 1: # maybe CoNLLx
        test_times = 11

        for test_time in xrange(test_times):
            block = sample(blocks, 1)[0]
            lines = block.split("\n")
            line = sample(lines, 1)[0]
            vote_box["unknown" if len(line.split()) != 0 else "conll"] += 1
    else:
        test_times = 11

        for test_time in xrange(test_times):
            lines = corpus.strip().split("\n")
            line = sample(lines, 1)[0]
            words = line.split()
            if len(words) > 1: # segment or postag
                test_item_times = 11
                sub_vote_box = {
                        "segment":  0,
                        "postag":   0,};
                for test_item_time in xrange(test_item_times):
                    if sample(words, 1)[0].find("_") != -1:
                        sub_vote_box["postag"] += 1
                    else:
                        sub_vote_box["segment"] += 1

                vote_box[_argmax(sub_vote_box)] += 1
            else:
                vote_box["plain"] += 1

    return _argmax(vote_box)

if __name__=="__main__":
    sample_1 = """这是一个中文语料。\n语料没有进行分词。"""
    sample_2 = """这 是 一个 中文 语料 。\n语料 经过 分词 处理。"""
    sample_3 = """这_AD 是_VV 一个_M 中文_NN 语料_NN 。_WP\n语料_NN 经过_VV 分词_NN 处理_VV 。_WP"""

    assert(detect(sample_1) == "plain");    print("pass");
    assert(detect(sample_2) == "segment");  print("pass");
    assert(detect(sample_3) == "postag");   print("pass");
