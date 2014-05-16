#!/usr/bin/env python

def Generalize(token, MATCHES):
    '''
    Generalize the token with regex rule.

    Parameters
    ----------
    token : str
        The token to be generalized
    MATCHES : list
        A list of tuple, two elements in each tuple. The first element
        is the matching regex and the second element is the name.

    Return
    ------
    type : str
        Get the type string.
    '''
    for MATCH in MATCHES:
        regex, name = MATCH
        if regex.match(token):
            return name
    return token
