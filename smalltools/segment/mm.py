#!/usr/bin/env python

def MaximumMatching(chars,
        lexicon,
        longest = 7,
        segment_character = False,
        encoding = "utf-8"):
    '''
    A simple maximum matching algorithm to detect word boundary from token

    Parameters
    ----------
    chars : str or unicode
        The input characters
    lexicon : str
        The lexicon
    longest : int
        The maximum length of potential word
    segment_character : bool
        If this flag is true, the unmatched character is considered as a
        single word. Otherwise, the contiguous unmatched characters are
        considered as a single word.
    encoding : str
        The encoding

    Return
    ------
    words: list
        Return a list of maximum matching words. Each element of the list
        is a tuple consists two objects, the word and a flag specify if 
        the word match lexicon
    '''

    if encoding is not None:
        chars = chars.decode(encoding)

    L = len(chars)
    word, words = "", []
    i = 0
    while i < L:
        found = False
        for j in xrange(min(i + longest, L), i, -1):
            candidate_word = chars[i:j]
            if encoding is not None:
                candidate_word = candidate_word.encode(encoding)
            if candidate_word in lexicon:
                if word != "":
                    words.extend([(word, False), (candidate_word, True)])
                else:
                    words.append((candidate_word, True))
                word = ""
                found = True
                i = j
                break
        if not found:
            ch = chars[i] if encoding is None else chars[i].encode(encoding)
            if segment_character:
                words.append((ch, False))
            else:
                word += ch
            i += 1

    if word != "":
        words.append((word, False))
    return words
