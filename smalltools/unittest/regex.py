# -*- coding: utf8 -*-
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from ..regex import reFloatNumber, \
                    reScientificFloatNumber, \
                    reURL

class UtilsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFloatRegex(self):
        self.assertTrue(reFloatNumber.match('1.0') is not None)
        self.assertTrue(reFloatNumber.match('1998') is not None)

    def testScientificFloatRegex(self):
        self.assertTrue(reScientificFloatNumber.match('1e10') is not None)
        self.assertTrue(reScientificFloatNumber.match('1.1e4') is not None)
        self.assertTrue(reScientificFloatNumber.match('10E4') is not None)

    def testURLRegex(self):
        self.assertTrue(reURL.match("www.google.com") is not None)
        self.assertTrue(reURL.match("http://www.google.com") is not None)
        self.assertTrue(reURL.match("https://www.google.com/") is not None)
        self.assertTrue(reURL.match("ftp://202.118.250.16/download?type=file") is not None)

if __name__=="__main__":
    main()
