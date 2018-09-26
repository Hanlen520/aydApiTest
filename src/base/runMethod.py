# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 11:27
# @Author  : Burrows
# @FileName: runMethod.py

"""封装requests请求方法"""

import requests

class RunMethod:
    def get_main(self, url, params, **kw):
        """封装requests.get方法"""
        if params is not None and params != "no":
            res = requests.get(url, params=params, **kw)
        else:
            res = requests.get(url, **kw)
        return res

    def post_main(self, url, data, **kw):
        """封装requests.post方法"""
        if data is not None and data != "no":
            res = requests.post(url, data=data, **kw)
        else:
            res = requests.post(url, **kw)
        return res


    def run_main(self, method, url, data, **kw):
        """封装主方法"""
        if method.lower() == "get":
            res = self.get_main(url, data, **kw)
        elif method.lower() == "post":
            res = self.post_main(url, data, **kw)
        else:
            res = "Do Not Support Method!"
            pass
        return res
        # return json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True)

if __name__ == "__main__":
    runmethod = RunMethod()
    url = "http://127.0.0.1:8000/api/user_login"
    method = "post"
    data = {"username": "admin", "password": "admin123456"}
    res = runmethod.run_main(method, url, data)
    print(res.text)
