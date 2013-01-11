#!/usr/bin/env python
#-*- coding:utf8 -*-
def dbc2sbc(ustring):
    """ 
    convert unicode string in double byte character
    to single byte character
    """
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
            rstring += unichr(inside_code)
    return rstring


def sbc2dbc(ustring):
    """ 
    convert unicode string in single byte character
    to double byte character
    """
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
    print sbc2dbc("xyz".decode("utf8")).encode("utf8")
    print dbc2sbc("ｘｙｚ".decode("utf8")).encode("utf8")
