# -*- coding: utf8 -*-
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from ..regex import reFloatNumber, \
                    reScientificFloatNumber

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

if __name__=="__main__":
    main()
