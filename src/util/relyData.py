# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 15:28
# @Author  : Burrows
# @FileName: relyData.py
"""处理关联数据"""

import jsonpath_rw
from jsonpath import jsonpath
import os

from base.operJson import OperJson


class RelyData:
    def __init__(self):
        self.rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.rely_data = self.rootpath + '/data' + '/pubData/' + 'relyData.tmp'
        self.op_json = OperJson()
        self.rely_dict = {}

    def get_rely_from_resp(self, key, resp):
        '''
        :param key: 响应中需要获取关联数据的key
        :param resp: 响应数据, dict
        :return: 关联值
        '''
        # jsonpath-rw解析数据
        # 响应中获取首个匹配到的key，返回一个list
        # data_list = jsonpath_rw.parse("E_testdata[*].{_key}".format(_key=key)).find(resp)
        # # 获取list数据的第一个值
        # data = [match.value for match in data_list][0]

        # jsonpath解析数据
        data_list = jsonpath(resp, '$..%s' % key)
        print(data_list)
        return data_list[0]

    def get_rely_from_file(self, key):
        '''
        :param key: 文件中需要获取关联数据的key
        '''
        data = self.op_json.read_jsondata(key)
        return data

    def write_rely_to_file(self, key, resp):
        '''
        :param key: 写入关联数据到文件
        :param resp: 响应数据, dict
        '''
        rely_data = self.get_rely_from_resp(key, resp)
        self.rely_dict[key] = rely_data
        self.op_json.append_data_to_jsonfile(self.rely_dict)
        return rely_data

if __name__ == '__main__':
    resp = {
'status': 200,
'message': 'success',
'E_testdata': [
    {'realname': 'burrows2', 'phone': '13700000002', 'email': 'burrows2@test.com', 'sign': False},
     {'realname': 'burrows3', 'phone': '13700000003', 'email': 'burrows3@test.com', 'sign': False},
     {'realname': 'burrows8', 'phone': '13700000008', 'email': 'burrows8@test.com', 'sign': False}
     ]
}

    key = "phone"
    rely_data = RelyData()
    data = rely_data.get_rely_from_resp(key, resp)
    print(data)
