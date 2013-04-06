from chartypes import sbc, dbc

def sbc2dbc(ch, encoding=None):
    """
    Convert single bit character to double bit character.
    Return double bit character in unicode
    """
    if encoding is not None:
        ch = ch.decode(encoding)

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

    try:
        idx = sbc["punc"].index(ch)
        return dbc["punc"][idx]
    except:
        pass

    try:
        idx = sbc["digit"].index(ch)
        return dbc["digit"][idx]
    except:
        pass

    return ch

def dbc2sbc(ch, encoding=None):
    """
    Convert double bit character to single bit character.
    Return single bit character in unicode.
    """
    if encoding is not None:
        ch = ch.decode(encoding)

    try:
        idx = dbc["digit"].index(ch)
        return sbc["digit"][idx % 10]
    except ValueError:
        pass

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

    try:
        idx = dbc["punc"].index(ch)
        return sbc["punc"][idx]
    except ValueError:
        pass

    return ch

def fast_dbc2sbc(ch, encoding=None):
    """ 
    A faster implement of convertion from double byte character
    to single byte character
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


