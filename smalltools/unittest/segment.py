# -*- coding: utf8 -*-
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from ..segment.word2labels import _BIstyle, _BIESstyle, _BB2B3IESstyle

class UtilsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWord2Tags(self):
        self.assertEquals(_BIstyle("word"),  ["B", "I", "I", "I"])
        self.assertEquals(_BIstyle("am"),    ["B", "I"])
        self.assertEquals(_BIstyle("I"),     ["B"])
        self.assertEquals(_BIESstyle("are"), ["B", "I", "E"])

if __name__=="__main__":
    main()
