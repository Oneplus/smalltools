import re
import sys

from sbcdbc import dbc2sbc, fast_dbc2sbc

URL=0
ENG=1
DIG=2
NONE=-1

_url_regex = re.compile("(https|ftp|file)://"
        "[-A-Za-z0-9+&@#/%?=~_|!:,.;]*"
        "[-A-Za-z0-9+&@#/%=~_|]")

_url_regex_2 = re.compile("[a-zA-Z0-9\-\.]+\."
        "(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU)")
_eng_word_regex = re.compile("([a-zA-Z]+)([\-'\.][a-zA-Z]+)*")
_digit_regex = re.compile("\d+")


def _is_url(word):
    if _url_regex.match(word) is not None:
        return True

    if _url_regex_2.match(word) is not None:
        return True

    return False

def _is_eng_word(word):
    if _eng_word_regex.match(word) is not None:
        return True
    return False

def _is_digit(word):
    if _digit_regex.match(word) is not None:
        return True
    return False

def wordtype(word, encoding=None, fast=False):
    if encoding is not None:
        word = word.decode(encoding)

    if fast:
        word = "".join([fast_dbc2sbc(ch) for ch in word])
    else:
        word = "".join([dbc2sbc(ch) for ch in word])

    if _is_url(word):
        return URL

    if _is_eng_word(word):
        return ENG

    if _is_digit(word):
        return DIG

    return NONE

if __name__=="__main__":
    print >> sys.stderr, "library is not runnable"
