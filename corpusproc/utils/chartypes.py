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

def chartype(ch, lvl=1, encoding=None):
    if encoding is not None:
        ch = ch.decode(encoding)

    if ch in dbc_lookup["uppercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_DBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_DBC, CHAR_LETTER_DBC_UPPERCASE]

    if ch in dbc_lookup["lowercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_DBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_DBC, CHAR_LETTER_DBC_LOWERCASE]

    # @NOTE: This part should be optimized
    if ch in sbc_lookup["uppercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_SBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_SBC, CHAR_LETTER_SBC_UPPERCASE]

    if ch in sbc_lookup["lowercase"]:
        if lvl == 1:
            return [CHAR_LETTER,]
        elif lvl == 2:
            return [CHAR_LETTER, CHAR_LETTER_SBC,]
        else:
            return [CHAR_LETTER, CHAR_LETTER_SBC, CHAR_LETTER_SBC_LOWERCASE]

    if ch in dbc_lookup["digit"]:
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

    if ch in sbc_lookup["digit"]:
        if lvl == 1:
            return [CHAR_DIGIT,]
        else:
            return [CHAR_DIGIT, CHAR_DIGIT_SBC,]

    if ch in dbc_lookup["punc"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        elif lvl == 2:
            return [CHAR_PUNC, CHAR_PUNC_NORMAL,]

    if ch in dbc_lookup["chinese-punc"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        else:
            return [CHAR_PUNC, CHAR_PUNC_CHINESE,]

    if ch in dbc_lookup["punc-ext"]:
        if lvl == 1:
            return [CHAR_PUNC,]
        else:
            return [CHAR_PUNC, CHAR_PUNC_EXT,]

    if ch in sbc_lookup["punc"]:
        return [CHAR_PUNC,]

    return [OTHER,]

