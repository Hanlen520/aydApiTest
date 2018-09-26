# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:34
# @Author  : Burrows
# @FileName: runTest.py

import unittest
import time

from base.runMethod import RunMethod
from base.readLogger import ReadLogger
from util.relyData import RelyData

class RunTest(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(RunTest, self).__init__(methodName)

        # 获取logger和run_log
        read_logger = ReadLogger()
        self.logger = read_logger.get_logger()
        self.run_log_src = read_logger.get_run_log()

        # 使用自封装requests
        self.run_method = RunMethod()

        # 使用自封装关联数据
        self.rely_data = RelyData()

    # @classmethod
    # def setUpClass(cls):
    #     print('开始测试'.center(50, '#'))
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print('结束测试'.center(50, '#'))

    # def setUp(self):
    #     self.logger.debug("start case...")
    #
    # def tearDown(self):
    #     self.logger.debug("end case...")

    def start(self, **kw):

        # 获取case数据
        case_id = kw.get('case_id')
        module = kw.get('module')
        url = kw.get('request').get('url')
        method = kw.get('request').get('method','get')  # 缺省get请求
        header = kw.get('request').get('header', '')  # 缺省headers为空
        cookie = kw.get('request').get('cookie', '')  # 缺省cookies为空
        data = kw.get('request').get('data', '')  # 缺省data为空
        validators = kw.get('validators')
        relyDataKey = kw.get('relyDataKey')  # 该接口被其他接口依赖关联字段
        relyDataVal = kw.get('relyDataVal')  # 该接口运行依赖关联字段
        start_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        start_timestamp = time.time()

        try:
            # 处理关联数据
            if relyDataVal is not None:
                for x in relyDataVal:
                    relyDataSrc = x.get('relyDataSrc')  # 关联字段
                    relyDataDes = x.get('relyDataDes')  # 依赖关联字段
                    rely_data = self.rely_data.get_rely_from_file(relyDataSrc)
                    data[relyDataDes] = rely_data

            self.logger.debug('开始测试 %s '.center(80, '#') % case_id)
            self.logger.debug('请求信息: '.center(50, '-'))
            self.logger.debug('请求时间: %s' % start_time)
            self.logger.debug('module: %s' % module)
            self.logger.debug('url: %s' % url)
            self.logger.debug('method: %s' % method)
            self.logger.debug('header: %s' % header)
            self.logger.debug('cookie: %s' % cookie)
            self.logger.debug('data: %s' % data)
            self.logger.debug('validators: %s' % validators)
            self.logger.debug('relyDataKey: %s' % relyDataKey)
            self.logger.debug('relyDataVal: %s' % relyDataVal)

            # 发送请求
            # 接口有异常的情况下，可能返回的不是json串，会报错
            res = self.run_method.run_main(method, url, data, cookies=cookie, headers=header)

            end_time = time.strftime("%Y-%m-%d_%H-%M-%S")
            end_timestamp = time.time()
            time_spend = '%.2f' % (end_timestamp - start_timestamp)

            self.logger.debug('响应信息: '.center(50, '-'))
            self.logger.debug('响应时间: %s' % end_time)
            self.logger.debug('响应耗时: %s' % time_spend)
            self.logger.info('响应码: %s' % res.status_code)
            self.logger.info('响应头: %s' % res.headers)

            # 查看是否包含 断言查看一次错误就停止，后面加入错误提示
            self.assertEqual(res.status_code, 200, msg='预计结果不符:http_code预期结果 200,实际结果【%s】' % (res.status_code))

            # 响应结果转json
            res = res.json()

            # 保存被关联数据
            if relyDataKey is not None:
                self.rely_data.write_rely_to_file(relyDataKey, res)

            # 断言
            for valid in validators:
                check = valid.get('check')  # 待检查字段
                expect = valid.get('expect')  # 预期值
                resp_data = res.get(check)
                if isinstance(expect, int):
                    self.assertEqual(expect, resp_data, msg='预计结果不符:【%s】预期结果【%s】,实际结果【%s】' % (check, expect, resp_data))
                if isinstance(expect, str):
                    self.assertIn(expect, resp_data, msg='预计结果不符:【%s】预期结果【%s】,实际结果【%s】' % (check, expect, resp_data))

            self.logger.info('响应内容: %s' % res)

        except Exception as e:
            self.logger.error('用例%s请求出错: %s' % (case_id, e))
            raise
        finally:
            self.logger.debug('结束测试 %s '.center(80, '#') % case_id)
