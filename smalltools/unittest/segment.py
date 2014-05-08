# -*- coding: utf8 -*-
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from ..segment.word2tags import BIstyle, BIESstyle, BB2B3IESstyle

class UtilsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWord2Tags(self):
        self.assertEquals(BIstyle("word"),  ["B", "I", "I", "I"])
        self.assertEquals(BIstyle("am"),    ["B", "I"])
        self.assertEquals(BIstyle("I"),     ["B"])
        self.assertEquals(BIESstyle("are"), ["B", "I", "E"])

if __name__=="__main__":
    main()
