'''
This modole implement a serial of functions related with single byte 
character and double byte character conversion.
'''
from settings import sbc, dbc

CONV_LETTER         = 0x0001
CONV_DIGIT          = 0x0002
CONV_CHINESE_DIGIT  = 0x0004
CONV_PUNC           = 0x0008

def sbc2dbc(ch, flags=0xffff, includes=[], excludes=[], encoding=None):
    '''
    Convert single bit character to double bit character.
    Return double bit character in unicode

    Parameters
    ----------
    ch : str or unicode
        The character
    flags : int
        The convertion flags
    includes : set
        If the input character is in the includes set, this function will
        try every possible conversion without caring the flags
    excludes : set
        If the input character is in the excludes set, this function will
        directly return the character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    '''
    if encoding is not None:
        ch = ch.decode(encoding)

    if ch in excludes:
        return ch

    be_included = ch in includes

    if flags & CONV_LETTER or be_included:
        try:
            idx = sbc["uppercase"].index(ch)
            return dbc["uppercase"][idx]
        except ValueError:
            pass

        try:
            idx = sbc["lowercase"].index(ch)
            return dbc["lowercase"][idx]
        except ValueError:
            pass

    if flags & CONV_PUNC or be_included:
        try:
            idx = sbc["punc"].index(ch)
            return dbc["punc"][idx]
        except:
            pass

    if flags & CONV_DIGIT or be_included:
        try:
            idx = sbc["digit"].index(ch)
            return dbc["digit"][idx]
        except:
            pass

    return ch


def dbc2sbc(ch, flags=0xffff, includes=[], excludes=[], encoding=None):
    '''
    Convert double bit character to single bit character.
    Return single bit character in unicode.

    Parameters
    ----------
    ch : str or unicode
        The character
    flags : int
        The convertion flags
    includes : set
        If the input character is in the includes set, this function will
        try every possible conversion without caring the flags
    excludes : set
        If the input character is in the excludes set, this function will
        directly return the character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    '''
    if encoding is not None:
        ch = ch.decode(encoding)

    if ch in excludes:
        return ch

    be_included = ch in includes

    if (flags & CONV_DIGIT and flags & CONV_CHINESE_DIGIT) or be_included:
        try:
            idx = dbc["digit"].index(ch) % 10
            return sbc["digit"][idx]
        except ValueError:
            pass


    if flags & CONV_DIGIT or be_included:
        try:
            idx = dbc["digit"].index(ch)
            return sbc["digit"][idx]
        except ValueError:
            pass
        except IndexError:
            pass

    if flags & CONV_LETTER or be_included:
        try:
            idx = dbc["uppercase"].index(ch)
            return sbc["uppercase"][idx]
        except ValueError:
            pass

        try:
            idx = dbc["lowercase"].index(ch)
            return sbc["lowercase"][idx]
        except ValueError:
            pass

    if flags & CONV_PUNC or be_included:
        try:
            idx = dbc["punc"].index(ch)
            return sbc["punc"][idx]
        except ValueError:
            pass

    return ch



def str_sbc2dbc(ustring, flags=0xffff, includes=[], excludes=[], encoding=None):
    '''
    Convert str in single byte to double byte character by character.
    It is very slow.

    Parameters
    ----------
    ustring : str or unicode
        The string
    flags : int
        The convertion flags
    includes : set
        If the input character is in the includes set, this function will
        try every possible conversion without caring the flags
    excludes : set
        If the input character is in the excludes set, this function will
        directly return the character
    encoding : str
        The encoding

    Return
    ------
    rstring : unicode
        The converted string
    '''
    if encoding is not None:
        ustring = ustring.decode(encoding)

    return ''.join([sbc2dbc(_, flags, includes, excludes, None) for _ in ustring])


def str_dbc2sbc(ustring, flags=0xffff, includes=[], excludes=[], encoding=None):
    '''
    Convert str in single byte to double byte character by character
    It is very slow.

    Parameters
    ----------
    ustring : str or unicode
        The string
    flags : int
        The convertion flags
    includes : set
        If the input character is in the includes set, this function will
        try every possible conversion without caring the flags
    excludes : set
        If the input character is in the excludes set, this function will
        directly return the character
    encoding : str
        The encoding

    Return
    ------
    rstring : unicode
        The converted string
    '''
    if encoding is not None:
        ustring = ustring.decode(encoding)

    return ''.join([dbc2sbc(_, flags, includes, excludes, None) for _ in ustring])


def fast_dbc2sbc(ch, encoding=None):
    """
    A faster implement of convertion from double byte character
    to single byte character

    Parameters
    ----------
    ch : str or unicode
        The character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    """
    if encoding is not None:
        ch = ch.decode(encoding)

    inside_code = ord(ch)

    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:
            # if the converted character is not
            # in range of single byte, convert back
            return ch
        return unichr(inside_code)

    return ch


def fast_sbc2dbc(ch, encoding=None):
    """
    A faster implement of convertion from single byte character
    to double byte character
 
    Parameters
    ----------
    ch : str or unicode
        The character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    """
    if encoding is not None:
        ch = ch.decode(encoding)

    inside_code=ord(ch)
    if inside_code<0x0020 or inside_code>0x7e:
        # if this code in range of single byte
        return ch
    else:
        # the convert formular is
        # SBC = DBC - 0xfee0
        if inside_code==0x0020:
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        return unichr(inside_code)

    return ch


def fast_str_dbc2sbc(ustring, encoding=None):
    """
    convert unicode string in double byte character
    to single byte character
 
    Parameters
    ----------
    ch : str or unicode
        The character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    """
    if encoding is not None:
        ustring = ustring.decode(encoding)

    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
            if inside_code<0x0020 or inside_code>0x7e:
                # if the converted character is not
                # in range of single byte, convert back
                rstring += uchar
            else:
                rstring+= unichr(inside_code)
    return rstring


def fast_str_sbc2dbc(ustring, encoding=None):
    """
    convert unicode string in single byte character
    to double byte character

    Parameters
    ----------
    ch : str or unicode
        The character
    encoding : str
        The encoding

    Return
    ------
    ch : unicode
        The converted character
    """
    if encoding is not None:
        ustring = ustring.decode(encoding)

    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:
            # if this code in range of single byte
            rstring += uchar
        else:
            # the convert formular is
            # SBC = DBC - 0xfee0
            if inside_code==0x0020:
                inside_code=0x3000
            else:
                inside_code+=0xfee0
            rstring += unichr(inside_code)

    return rstring

if __name__=="__main__":
    print str_sbc2dbc("1988", encoding="utf-8").encode("utf-8")
