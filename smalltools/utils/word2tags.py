# word2tags.py
#
# Provide function to convert word to character based
# word segmentation tags in different styles.
#
# Example:
#
#   BIstyle("word") = ["B", "I", "I", "I"]
#   BIESstyle("word") = ["B", "I", "I", "E"]
#
# and so on.

def BIstyle(word, encoding=None):
    if encoding is not None:
        word = word.decode(encoding)

    ret = []
    for i, c in enumerate(word):
        if i == 0:
            ret.append( "B" )
        else:
            ret.append( "I" )

    return ret

def BIESstyle(word, encoding=None):
    if encoding is not None:
        word = word.decode(encoding)

    ret = []
    if len(word) == 1:
        ret.append("S")
    else:
        for i, c in enumerate(word):
            if i == 0:
                ret.append("B")
            elif i == len(word) - 1:
                ret.append("E")
            else:
                ret.append("I")
    return ret

def BB2B3IESstyle(word, encoding=None):
    if encoding is not None:
        word = word.decode(encoding)

    ret = []
    if len(word) == 1:
        ret.append("S")
    else:
        for i, c in enumerate(word):
            if i == 0:
                ret.append("B")
            elif i == len(word) - 1:
                ret.append("E")
            elif i == 1:
                ret.append("B2")
            elif i == 2:
                ret.append("B3")
            else:
                ret.append("I")
    return ret

