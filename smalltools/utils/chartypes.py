# -*- coding: utf8 -*-
from settings import dbc, dbc_lookup, sbc_lookup
from settings import \
        CHAR_LETTER, \
        CHAR_LETTER_DBC, CHAR_LETTER_SBC, \
        CHAR_LETTER_DBC_UPPERCASE, CHAR_LETTER_DBC_LOWERCASE, \
        CHAR_LETTER_SBC_UPPERCASE, CHAR_LETTER_SBC_LOWERCASE, \
        CHAR_DIGIT, \
        CHAR_DIGIT_DBC, CHAR_DIGIT_SBC, \
        CHAR_DIGIT_DBC_CL1, CHAR_DIGIT_DBC_CL2, CHAR_DIGIT_DBC_CL3, \
        CHAR_PUNC, \
        CHAR_PUNC_DBC, CHAR_PUNC_SBC, \
        CHAR_PUNC_DBC_NORMAL, CHAR_PUNC_DBC_CHINESE, CHAR_PUNC_DBC_EXT, \
        CHAR_OTHER

CHK_LETTER = 0x0001
CHK_DIGIT  = 0x0002
CHK_PUNC   = 0x0004

def chartype(ch, flags=0xffff, lvl=1, encoding=None):
    '''
    Get type of character

    Parameters
    ----------
    ch : str or unicode
        The character
    flags: int
        The check flags. By default, all the three types are checked.
    lvl : int
        The detect level
    encoding : str
        The encoding

    Return
    ------
    chartype : list(int
        The chartype in different level
    '''
    if encoding is not None:
        ch = ch.decode(encoding)

    if (flags & CHK_LETTER) and ch in dbc_lookup["uppercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_DBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_DBC, CHAR_LETTER_DBC_UPPERCASE]

    if (flags & CHK_LETTER) and ch in dbc_lookup["lowercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_DBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_DBC, CHAR_LETTER_DBC_LOWERCASE]

    # @NOTE: This part should be optimized
    if (flags & CHK_LETTER) and ch in sbc_lookup["uppercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_SBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_SBC, CHAR_LETTER_SBC_UPPERCASE]

    if (flags & CHK_LETTER) and ch in sbc_lookup["lowercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_SBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_SBC, CHAR_LETTER_SBC_LOWERCASE]

    if (flags & CHK_DIGIT) and ch in dbc_lookup["digit"]:
        if lvl == 1:
            return [CHAR_DIGIT,]
        elif lvl == 2:
            return [CHAR_DIGIT, CHAR_DIGIT_DBC,]
        else:
            idx = dbc["digit"].index(ch) / 10
            if idx == 0:
                return [CHAR_DIGIT, CHAR_DIGIT_DBC, CHAR_DIGIT_DBC_CL1,]
            elif idx == 1:
                return [CHAR_DIGIT, CHAR_DIGIT_DBC, CHAR_DIGIT_DBC_CL2,]
            elif idx == 2:
                return [CHAR_DIGIT, CHAR_DIGIT_DBC, CHAR_DIGIT_DBC_CL3,]

    if (flags & CHK_DIGIT) and ch in sbc_lookup["digit"]:
        if lvl == 1:
            return [CHAR_DIGIT,]
        else:
            return [CHAR_DIGIT, CHAR_DIGIT_SBC,]

    if (flags & CHK_PUNC) and ch in dbc_lookup["punc"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        elif lvl == 2:
            return [CHAR_PUNC, CHAR_PUNC_NORMAL,]

    if (flags & CHK_PUNC) and ch in dbc_lookup["chinese-punc"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        else:
            return [CHAR_PUNC, CHAR_PUNC_CHINESE,]

    if (flags & CHK_PUNC) and ch in dbc_lookup["punc-ext"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        else:
            return [CHAR_PUNC, CHAR_PUNC_EXT,]

    if (flags & CHK_PUNC) and ch in sbc_lookup["punc"]:
        return [CHAR_PUNC,]

    return [CHAR_OTHER,]

