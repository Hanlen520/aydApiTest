# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:34
# @Author  : Burrows
# @FileName: runTest.py

'''封装公共测试流'''

import unittest
import time

from base.runMethod import RunMethod
from base.readLogger import ReadLogger
from util.relyData import RelyData

class RunTest(unittest.TestCase, unittest.SkipTest):
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

        self.case_id = ''  # 用例id
        self.desc = ''  # 用例描述
        self.req_msg = {'request': {}, '\nresponse': {}}  # 用例基本信息

    def skipTest(self, reason):
        raise unittest.SkipTest

    def getCasePro(self):
        return self.case_id, self.desc

    def getCaseMsg(self):
        return self.req_msg

    def start(self, url, uri, method, api_name, header, cookie, **kw):

        # 获取case数据
        skip = kw.get('skip', '0')  # skip默认值为0，为1表示跳过该case
        self.case_id = kw.get('case_id')
        self.desc = kw.get('desc')
        api_name = api_name
        url = url + uri
        method = method
        header = header
        cookie = cookie
        # header = kw.get('request').get('header', '')  # 缺省headers为空
        # cookie = kw.get('request').get('cookie', '')  # 缺省cookies为空
        # data = kw.get('request').get('data', '')  # 缺省data为空
        data = kw.get('request_data')
        validators = kw.get('validators')
        relyDataExport = kw.get('relyDataExport')  # 关联输出，即该接口响应返回被其他接口关联字段
        relyDataImport = kw.get('relyDataImport')  # 关联引入，即该接口运行所需的关联字段设置
        start_time = time.strftime("%Y/%m/%d %H:%M:%S")
        start_timestamp = time.time() * 1000  # ms

        self.req_msg.get('request').setdefault('\nreq.url', url)
        self.req_msg.get('request').setdefault('\nreq.method', method)
        self.req_msg.get('request').setdefault('\nreq.header', header)
        self.req_msg.get('request').setdefault('\nreq.cookie', cookie)
        self.req_msg.get('request').setdefault('\nreq.data', data)
        self.req_msg.get('request').setdefault('\nreq.validators', validators)
        self.req_msg.get('request').setdefault('\nreq.relyDataExport', relyDataExport)
        self.req_msg.get('request').setdefault('\nreq.relyDataImport', str(relyDataImport) + '\n')

        if int(skip) == 1:
            self.logger.debug('跳过用例   ：%s(%s)' % (self.case_id, self.desc))
            self.skipTest('skip case')

        try:
            # 处理关联数据
            if relyDataImport is not None:
                for x in relyDataImport:
                    relyDataSrc = x.get('relyDataSrc')  # 关联字段
                    relyDataDes = x.get('relyDataDes')  # 依赖关联字段
                    rely_data = self.rely_data.get_rely_from_file(relyDataSrc)
                    data[relyDataDes] = rely_data

            self.logger.debug('用例编号   ：%s ' % self.case_id)
            self.logger.debug('接口名称   : %s' % api_name)
            self.logger.debug('用例描述   : %s' % self.desc)
            self.logger.debug('请求时间   : %s' % start_time)
            self.logger.debug(' 请求信息 '.center(50, '-'))
            self.logger.debug('url        : %s' % url)
            self.logger.debug('method     : %s' % method)
            self.logger.debug('header     : %s' % header)
            self.logger.debug('cookie     : %s' % cookie)
            self.logger.debug('请求数据   : %s' % data)
            self.logger.debug('断言设置   : %s' % validators)
            self.logger.debug('关联输出   : %s' % relyDataExport)
            self.logger.debug('关联引入   : %s' % relyDataImport)

            # 发送请求
            # 接口有异常的情况下，可能返回的不是json串，会报错
            res = self.run_method.run_main(method, url, data, cookies=cookie, headers=header)

            end_time = time.strftime("%Y/%m/%d %H:%M:%S")
            end_timestamp = time.time() * 1000  # ms
            time_spend = '%.2f' % (end_timestamp - start_timestamp)  # ms精度

            self.logger.debug(' 响应信息 '.center(50, '-'))
            self.logger.debug('响应时间   : %s' % end_time)
            self.logger.debug('响应耗时   : %s ms' % time_spend)
            self.logger.debug('响应码     : %s' % res.status_code)
            self.logger.debug('响应头     : %s' % res.headers)

            self.req_msg.get('\nresponse').setdefault('\nresp.status_code', res.status_code)
            self.req_msg.get('\nresponse').setdefault('\nresp.headers', res.headers)

            # 查看是否包含 断言查看一次错误就停止，后面加入错误提示
            self.assertEqual(res.status_code, 200, msg='预计结果不符:http_code预期结果 200,实际结果【%s】' % (res.status_code))

            # 响应结果转json
            res = res.json()
            self.req_msg.get('\nresponse').setdefault('\nresp.json', str(res) + '\n')

            # 保存被关联数据
            if relyDataExport is not None:
                for x in relyDataExport:
                    relyKey = x.get('relyKey')
                    keepKey = x.get('keepKey')
                    self.rely_data.write_rely_to_file(relyKey, keepKey, res)

            # 断言
            for valid in validators:
                check = valid.get('check')  # 待检查字段
                expect = valid.get('expect')  # 预期值
                resp_data = res.get(check)
                if isinstance(expect, int):
                    self.assertEqual(expect, resp_data, msg='预计结果不符:【%s】预期结果【%s】,实际结果【%s】' % (check, expect, resp_data))
                if isinstance(expect, str):
                    self.assertIn(expect, resp_data, msg='预计结果不符:【%s】预期结果【%s】,实际结果【%s】' % (check, expect, resp_data))

            self.logger.debug('响应内容   : %s' % res)

        except Exception as e:
            self.logger.debug('响应内容   : %s' % res)
            self.logger.error('错误信息   : %s' % e)
            raise
        # finally:
        #     self.logger.debug('结束测试 %s ' % self.case_id)
