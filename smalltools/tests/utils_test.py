# -*- coding: utf8 -*-
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from ..utils import chartype
from ..utils import wordtype
from ..utils import sbc2dbc, dbc2sbc,\
        fast_sbc2dbc, fast_dbc2sbc, \
        fast_str_dbc2sbc

from ..utils.chartypes import \
        CHAR_LETTER, CHAR_LETTER_DBC, CHAR_LETTER_DBC_UPPERCASE, \
        CHAR_DIGIT, CHAR_DIGIT_SBC 

from ..utils.wordtypes import URL, ENG, DIG, NONE

from ..utils.word2tags import BIstyle, BIESstyle, BB2B3IESstyle

class UtilsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSbc2Dbc(self):
        self.assertEquals(sbc2dbc("a"), u"ａ")
        self.assertEquals(sbc2dbc("A"), u"Ａ")
        self.assertEquals(sbc2dbc("2"), u"２")
        self.assertEquals(sbc2dbc("!"), u"！")

    def testDbc2Sbc(self):
        self.assertEquals(dbc2sbc(u"ａ"), "a")
        self.assertEquals(dbc2sbc("ａ", "utf8"), "a")
        self.assertEquals(dbc2sbc(u"１"), "1")
        self.assertEquals(dbc2sbc("１", "utf8"), "1")
        self.assertEquals(dbc2sbc(u"一"), "1")
        self.assertEquals(dbc2sbc(u"？"), "?")
        self.assertEquals(dbc2sbc("？", "utf8"), "?")
        self.assertEquals(dbc2sbc(u"Ａ"), "A")
        self.assertEquals(dbc2sbc("Ａ", "utf8"), "A")

    def testFastSbc2Dbc(self):
        self.assertEquals(fast_sbc2dbc("a"), u"ａ")
        self.assertEquals(fast_sbc2dbc("A"), u"Ａ")
        self.assertEquals(fast_sbc2dbc("2"), u"２")
        self.assertEquals(fast_sbc2dbc("!"), u"！")

    def testFastDbc2Sbc(self):
        self.assertEquals(fast_dbc2sbc(u"ａ"), "a")
        self.assertEquals(fast_dbc2sbc("ａ", "utf8"), "a")
        self.assertEquals(fast_dbc2sbc(u"１"), "1")
        self.assertEquals(fast_dbc2sbc("１", "utf8"), "1")
        self.assertEquals(fast_dbc2sbc(u"？"), "?")
        self.assertEquals(fast_dbc2sbc("？", "utf8"), "?")
        self.assertEquals(fast_dbc2sbc(u"Ａ"), "A")
        self.assertEquals(fast_dbc2sbc("Ａ", "utf8"), "A")

    def testCharType(self):
        self.assertEquals(chartype(u"Ａ")[0], CHAR_LETTER)
        self.assertEquals(chartype(u"Ａ", lvl=2)[1], CHAR_LETTER_DBC)
        self.assertEquals(chartype(u"Ａ", lvl=3)[2], CHAR_LETTER_DBC_UPPERCASE)
        self.assertEquals(chartype("1", lvl=2)[1], CHAR_DIGIT_SBC)

    def testWordType(self):
        self.assertEquals(wordtype("John"), ENG)
        self.assertEquals(wordtype(u"ｄｏｎ＇ｔ"), ENG)
        #self.assertEquals(wordtype("http://oneplus.info"), URL)
        #self.assertEquals(wordtype("1942"), DIG)
        #self.assertEquals(wordtype(u"１９４２"), DIG)
        #self.assertEquals(wordtype(u"十一"), DIG)

    def testFastStrDbc2Sbc(self):
        self.assertEquals(fast_str_dbc2sbc(u"Ａ１ｂ"), "A1b")

    def testWord2Tags(self):
        self.assertEquals(BIstyle("word"),  ["B", "I", "I", "I"])
        self.assertEquals(BIstyle("am"),    ["B", "I"])
        self.assertEquals(BIstyle("I"),     ["B"])
        self.assertEquals(BIESstyle("are"), ["B", "I", "E"])

if __name__=="__main__":
    main()
