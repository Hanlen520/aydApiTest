# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:11
# @Author  : Burrows
# @FileName: users.py

import unittest
from unittest import SkipTest
import ddt
import os

from common.runTest import RunTest
from base.readLogger import ReadLogger

rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
yamlDir = rootDir + '\\' + 'data' + '\\' + 'caseData' + '\\'

url = 'http://192.168.102.111:8000'
header = {'Accept': 'application/json, text/javascript, */*; q=0.01'}
cookie = {}
count = 0
className = 'Users'

@ddt.ddt
class Users(RunTest):
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

    @ddt.file_data(yamlDir + r'login.yaml')
    @ddt.unpack
    def test_login(self, **kw):
        self.start(url=url, uri='/api/user_login', method='POST', api_name='用户登录', header=header, cookie=cookie, **kw)

    # @unittest.skip
    @ddt.file_data(yamlDir + r'adder_guest.yaml')
    @ddt.unpack
    def test_adder_guest(self, **kw):
        self.start(url=url, uri='/api/add_guest', method='POST', api_name='添加嘉宾', header=header, cookie=cookie, **kw)

    @ddt.file_data(yamlDir + r'get_guest.yaml')
    @ddt.unpack
    def test_get_guest(self, **kw):
        self.start(url=url, uri='/api/get_guest_list', method='GET', api_name='查询嘉宾', header=header, cookie=cookie, **kw)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(Users))
    runner = unittest.TextTestRunner()
    runner.run(suite)
