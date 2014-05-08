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

def _BIstyle(word):
    ret = []
    for i, c in enumerate(word):
        if i == 0:
            ret.append( "B" )
        else:
            ret.append( "I" )

    return ret

def _BIESstyle(word):
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

def _BB2B3IESstyle(word):
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


def CharactersToLabels(word, style = 4):
    '''
    Convert characters to label, specified by different style of labels.

    Parameters
    ----------
    word : list
        The list of characters
    style : int
        Use to specify the labeling style

    Return
    ------
    list
        A list of labels
    '''
    if style == 2:
        return _BIstyle(word)
    elif style == 4:
        return _BIESstyle(word)
    elif style == 6:
        return _BB2B3IESstyle(word)


def WordToLabels(token,
                 escapespace = True,
                 regex = False,
                 MATCHES = [],
                 style = 4,
                 encoding = "utf-8"):
    '''
    Convert word token to segmentation labels. Different styles are implemented.

    Parameters
    ----------
    token : str
        The word token
    escapespace : bool
        If ``escapespace`` is set **True**, the space in the word are considered
        as a separator.
    regex: bool
        If ``regex`` is set **True**, the word token is not simplely separated 
        character by character. But use the provided regular expression to match
        certain sequence of the token.
    MATCHES: list
        A list of regex. They are only actived when the ``regex`` is **True**.

    Return
    ------
    list
        The list of list, each has two elements: ``label`` and ``character``
    '''
    ret = []
    if escapespace and regex:
        for seq in token.split():
            chars = WordToCharacterWithRegex(seq, MATCHES, encoding)
            labels = CharactersToLabels(chars)
            ret.extend([[label, ch] for ch, label in zip(chars, labels)])
    elif escapespace and not regex:
        for seq in token.split():
            chars = WordToCharacters(seq, encoding)
            labels = CharactersToLabels(chars)
            ret.extend([[label, ch] for ch, label in zip(chars, labels)])
    elif not escapespace and regex:
        chars = WordToCharacterWithRegex(seq, MATCHES, encoding)
        labels = CharactersToLabels(chars)
        ret.extend([[label, ch] for ch, label in zip(chars, labels)])
    else:
        chars = WordToCharacters(seq, encoding)
        labels = CharactersToLabels(chars)
        ret.extend([[label, ch] for ch, label in zip(chars, labels)])
    return ret
