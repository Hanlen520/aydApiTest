# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:11
# @Author  : Burrows
# @FileName: events.py

import unittest
import ddt
import os

from common.runTest import RunTest

rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
yamlDir = rootDir + '\\' + 'data' + '\\' + 'caseData' + '\\'


@ddt.ddt
class Events(RunTest):
    # ddt读文件，获取文件内容，循环调用函数，并且传给下面函数的如kw中，有多少条数据循环调用多少次测试函数
    @ddt.file_data(yamlDir + r'add_event.yaml')
    @ddt.unpack
    def test_add_event(self, **kw):
        self.start(**kw)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Events))
    runner = unittest.TextTestRunner()
    runner.run(suite)
