# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 16:30
# @Author  : Burrows
# @FileName: operJson.py
"""封装操作json文件数据的方法"""

import json
import os


class OperJson:
    def __init__(self, filename=None):
        self.rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if filename is None:
            relyName = 'relyData.json'  # 默认操作关联文件
        else:
            relyName = filename
        self.rely_data = self.rootpath + '\\' + 'data' + '\\' + 'pubData' + '\\' + relyName
        # print(self.rely_data)
        if_exists = os.path.exists(self.rely_data)
        if if_exists is False:
            self.setup_data()

    def read_json(self):
        """读取json文件数据"""
        # 默认使用关联文件
        with open(self.rely_data) as fp:
            json_data = json.load(fp)
            return json_data

    def read_jsondata(self, key=None):
        """读取jsondata数据"""
        if key is None:
            return self.read_json()
        else:
            return self.read_json().get(key)

    def append_data_to_jsonfile(self, data):
        """将指定的数据{}追加写入到json文件"""
        with open(self.rely_data) as f:
            src_data = json.load(f)

        for i in data:
            src_data[i] = data[i]

        json_obj = json.dumps(src_data, ensure_ascii=False, indent=2, sort_keys=True)

        with open(self.rely_data, 'w') as fw:
            fw.write(json_obj)

    def setup_data(self):
        """初始化rele_data.json数据"""
        with open(self.rely_data, 'w') as fp:
            fp.write(json.dumps({}))

if __name__ == "__main__":
    test_data = {'e': '5555', 'f': '6666'}
    test_data2 = {'e1': '33', 'f1': '22'}

    op_json = OperJson()
    # # print(op_json.read_jsondata("hehe"))
    # op_json.append_data_to_jsonfile(test_data)
    # op_json.append_data_to_jsonfile(test_data2)
    op_json.setup_data()



