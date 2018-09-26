# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 10:18
# @Author  : Burrows
# @FileName: start.py
'''
 ddt + yaml + request 驱动demo,以发布会登录为实例
'''

import unittest
import os
import sys
import time
import configparser

from BeautifulReport import BeautifulReport
from base.operFile import OperFile
from base.operSendmail import SendEmail

rootDir = os.path.dirname(os.path.abspath(__file__))
yamlDir = rootDir + '\\' + 'data' + '\\' + 'caseData' + '\\'
case_dir = rootDir + '\\' + 'src' + '\\' + 'cases' + '\\'
conf_file = rootDir + '\\' + 'conf' + '\\' + 'conf.ini'
log_path = rootDir + '\\' + 'log' + '\\' + 'run.log'

# 自动匹配用例作为testSuite
discover = unittest.defaultTestLoader.discover(case_dir, pattern='users.py')
# discover = unittest.defaultTestLoader.discover(case_dir, pattern='*.py')

# 发送邮件，附件内容为测试概览报告和测试详细报告
def sendmail(run_proj_ins=None):
    cf = configparser.ConfigParser()
    cf.read(conf_file)
    smtp_server = cf.get('email-conf', 'smtp_server')           # smtp服务器
    send_user = cf.get('email-conf', 'sender')       # 登录邮箱
    password = cf.get('email-conf', 'password')                # 登录密码，如果是第三方邮箱如163，需要用授权码登录
    if run_proj_ins is None:
        receiver_list = cf.get('email-conf', 'receiver')
    elif run_proj_ins in 'events':
        receiver_list = cf.get('email-conf', 'receiver_events')
    elif run_proj_ins in 'users':
        receiver_list = cf.get('email-conf', 'receiver_users')
    elif run_proj_ins in 'shop':
        receiver_list = cf.get('email-conf', 'receiver_shop')
    else:
        receiver_list = cf.get('email-conf', 'receiver')
    sub = "接口自动化测试报告"
    content="""
        测试邮件头
    """
    sen = SendEmail(smtp_server, send_user, password, receiver_list)
    sen.send_mail(sub, content, log_new, reportName)


if __name__ == "__main__":
    # 初始化运行数据
    # print(discover)
    now = time.strftime("%Y_%m_%d-%H_%M_%S")

    reportDir = './report/' + 'report_{_now}'.format(_now=now)
    os.mkdir(reportDir)
    reportName = reportDir + '/' + now + '_result.html'

    # 初始化接口测试数据
    # test_data.init_data()

    # 初始化日志
    op_file = OperFile()
    op_file.trunc_file(log_path)

    # 运行测试
    args_list = sys.argv
    run_proj = None
    if len(args_list) == 1:
        pass
    elif len(args_list) > 2:
        print('args num error!')
        sys.exit(1)
    elif args_list[1] in 'events':
        print('test events...')
        run_proj = "events"
    elif args_list[1] in 'users':
        print('test users...')
        run_proj = "users"
    elif args_list[1] in 'shop':
        print('test shop...')
        run_proj = "shop"
    else:
        print('args error!')
        sys.exit(1)

    # 自动发现方式运行用例
    with open(reportName, 'wb') as fp:
        result = BeautifulReport(discover)
        # 默认在当前路径下，可以加log_path
        result.report(filename=reportName, description='接口测试')

    # suite添加caseClass形式新增测试用例
    # suite = unittest.TestSuite()
    # suite.addTests(unittest.makeSuite(MyCase))
    # result = BeautifulReport(suite)
    # # 默认在当前路径下，可以加log_path
    # result.report(filename='mpp测试报告', description='描述部分', log_path='.')

    # 恢复环境
    log_new = reportDir + '\\' + 'run.log'
    op_file.copy_file(log_path, log_new)

    # 发送邮件
    # sendmail()
