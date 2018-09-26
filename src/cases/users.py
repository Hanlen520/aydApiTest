# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:11
# @Author  : Burrows
# @FileName: users.py

import unittest
import ddt
import os

from common.runTest import RunTest

rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
yamlDir = rootDir + '\\' + 'data' + '\\' + 'caseData' + '\\'

@ddt.ddt
class Users(RunTest):
    @ddt.file_data(yamlDir + r'login.yaml')
    @ddt.unpack
    def test_login(self, **kw):
        self.start(**kw)

    @ddt.file_data(yamlDir + r'adder_guest.yaml')
    @ddt.unpack
    def test_adder_guest(self, **kw):
        self.start(**kw)

    @ddt.file_data(yamlDir + r'get_guest.yaml')
    @ddt.unpack
    def test_get_guest(self, **kw):
        self.start(**kw)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Users))
    runner = unittest.TextTestRunner()
    runner.run(suite)
