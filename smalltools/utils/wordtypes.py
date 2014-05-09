import re
import sys

from sbcdbc import dbc2sbc, fast_dbc2sbc

URL=0x0001
ENG=0x0002
DIG=0x0004
NONE=0x0000

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


CHK_URL = 0x0001
CHK_ENGLISH = 0x0002
CHK_NUMERICAL = 0x0004

def wordtype(token, flags=0xffff, encoding=None, d2s = False, fast = False):
    '''
    Detect word's type

    Parameters
    ----------
    token : str or unicode
        The input string token
    flags : int
        The actived check
    d2s : bool
        Specify to conduct double byte to single byte conversion
    fast : bool
        Specify to use fast ``dbc2sbc``

    Return
    ------
    wordtype : int
        The type of word
    '''
    if encoding is not None:
        word = word.decode(encoding)

    if dbc2sbc:
        if fast:
            word = "".join([fast_dbc2sbc(ch, encoding=None) for ch in word])
        else:
            word = "".join([dbc2sbc(ch, encoding=None) for ch in word])

    if (flag & CHK_URL) and _is_url(word):
        return URL

    if (flag & CHK_ENGLISH) and _is_eng_word(word):
        return ENG

    if (flag & CHK_NUMERICAL) and _is_digit(word):
        return DIG

    return NONE

if __name__=="__main__":
    print >> sys.stderr, "library is not runnable"
