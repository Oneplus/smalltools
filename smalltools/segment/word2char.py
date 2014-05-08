#!/usr/bin/env python
# -*- coding: utf-8 -*-

def WordToCharacters(token, encoding="utf-8"):
    '''
    Convert word to characters

    Parameters
    ----------
    token : str
        The input string token
    encoding : str
        The encoding

    Return
    ------
    ret : list(str)
        The list of characters
    '''
    ret = []
    for ch in token.decode(encoding):
        ret.append(ch.encode(encoding))
    return ret



def WordToCharactersWithRegex(token, MATCHES, encoding="utf-8"):
    '''
    Convert word to characters, if certain part of the token matches
    by the regex, this part is treated as a single word.

    Parameters
    ----------
    token : str
        The input string token
    MATCHES : list(re)
        The predefined regex rules
    encoding : str
        The encoding

    Return
    ------
    ret : list(str)
        The list of characters
    '''
    ret = []
    start = 0
    matches = []
    for MATCH in MATCHES:
        for m in MATCH.finditer(token):
            matches.append((m.start(), m.end()))
    matches.sort(key=lambda l: (l[0], -l[1]))

    start = 0
    for s, e in matches:
        # To handle the overlap regex
        if start > s:
            continue
        between = token[start: s]
        assert(" " not in between)
        ret.extend([ch.encode(encoding) for ch in between.decode(encoding)])
        ret.append(token[s: e])
        start = e

    if start < len(token):
        between = token[start:]
        assert(" " not in between)
        ret.extend([ch.encode(encoding) for ch in between.decode(encoding)])

    return ret


if __name__=="__main__":
    import re
    print "|".join(WordToCharacters("星展集团-DBSBank"))
    print "|".join(WordToCharactersWithRegex("星展集团-DBSBank", [re.compile("\w+")]))
