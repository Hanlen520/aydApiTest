# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:11
# @Author  : Burrows
# @FileName: events.py

import unittest
from unittest import SkipTest
import ddt
import os

from common.runTest import RunTest
from base.readLogger import ReadLogger

rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
yamlDir = rootDir + '\\' + 'data' + '\\' + 'caseData' + '\\'
#
# read_logger = ReadLogger()
# logger = read_logger.get_logger()

url = 'http://192.168.102.111:8000'
header = {'Accept': 'application/json, text/javascript, */*; q=0.01'}
cookie = {}
count = 0  # 统计运行用例总数
className = 'Events'
# count_pass = 0
# count_skip = 0
# count_fail = 0
# count_fail_list = []

@ddt.ddt
class Events(RunTest):
    # @classmethod
    # def setUpClass(cls):
    #     logger.debug('开始测试%s类'.center(100, '+') % className)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     logger.debug('结束测试%s类,统计用例总数:%s'.center(100, '+') % (className, globals()['count']))

    def setUp(self):
        globals()['count'] += 1
        self.logger.debug("start %s case %s...".center(80, '#') % (className, count))

    def tearDown(self):
        self.logger.debug("end %s case %s...".center(80, '#') % (className, count))

    @ddt.file_data(yamlDir + r'add_event.yaml')
    @ddt.unpack
    def test_add_event(self, **kw):
        self.start(url=url, uri='/api/add_event', method='POST', api_name='添加发布会', header=header, cookie=cookie, **kw)

    # 单个接口测试demo
    # ddt读文件，获取文件内容，循环调用函数，并且传给下面函数的如kw中，有多少条数据循环调用多少次测试函数
    # @ddt.file_data(yamlDir + r'add_event.yaml')
    # @ddt.unpack
    # def test_add_event(self, **kw):
    #     try:
    #         self.start(url=url, uri='/api/add_event', method='POST', api_name='添加发布会', header=header, cookie=cookie, **kw)
    #         globals()['count_pass'] += 1
    #     except SkipTest:
    #         globals()['count_skip'] += 1
    #         raise
    #     except Exception:
    #         globals()['count_fail'] += 1
    #         globals()['count_fail_list'].append(count)
    #         raise

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Events))
    runner = unittest.TextTestRunner()
    runner.run(suite)
