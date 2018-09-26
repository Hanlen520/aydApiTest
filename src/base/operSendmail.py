# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 11:42
# @Author  : Burrows
# @FileName: new_htmlfile.py

""" 工具类，封装邮件发送操作 """
import os
import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将src路径加入环境变量

class SendEmail:
    def __init__(self, smtp_server, send_user, password, receiver_list):
        self.receiver_list = receiver_list.split(',')
        self.smtp_server = smtp_server  # smtp服务器
        self.send_user = send_user   # 登录邮箱
        self.password = password  # 登录密码，如果是第三方邮箱如163，需要用授权码登录

    # 发送邮件函数类
    def send_mail(self,sub, content, log_file=None, report=None):
        '''
        :param
            sub:      邮件主题
            content:  邮件内容
            log_file: 日志路径
            report:   报告路径
        '''
        user = "InterfaceTester" + "<" + self.send_user + ">"   # 发件人命名
        msgRoot = MIMEMultipart()       # 构造MIMEMultipart对象做为根容器
        msgRoot['Subject'] = sub                 # 主题
        msgRoot['From'] = user                   # 发件人
        msgRoot['To'] = ';'.join(self.receiver_list)  # 收件人邮箱，多人邮箱以 a@a.com;b@b.com 的形式排列

        # 构造邮件文本
        puretext = MIMEText(content, 'html', 'utf-8')  # plain
        msgRoot.attach(puretext)

        # 中文附件 - 日志
        log_name = u"运行时日志.log"                                           # 附件源
        log_file = open(log_file, 'rb').read()
        att2 = MIMEBase('application', 'octet-stream')                           # 构造MIMEText对象做为邮件显示内容并附加到根容器
        att2.set_payload(log_file)
        att2.add_header('Content-Disposition', 'attachment', filename=('gbk', '', log_name))
        encoders.encode_base64(att2)
        msgRoot.attach(att2)

        # 中文附件 - 报告
        report_name = u"测试报告.html"                                           # 附件源
        report_file = open(report, 'rb').read()
        att2 = MIMEBase('application', 'octet-stream')                           # 构造MIMEText对象做为邮件显示内容并附加到根容器
        att2.set_payload(report_file)
        att2.add_header('Content-Disposition', 'attachment', filename=('gbk', '', report_name))
        encoders.encode_base64(att2)
        msgRoot.attach(att2)

        # 非中文附件
        # sendfile2 = open(htmlFile,'rb').read()                           # 附件源
        # part = MIMEText(sendfile2,'base64', 'utf-8')                          # 构造MIMEText对象做为邮件显示内容并附加到根容器
        # part["Content-Type"] = 'application/octet-stream'                     # 附件格式
        # part["Content-Disposition"] = 'attachment; filename='+htmlFile        # 附件命名
        # msgRoot.attach(part)

        # 连接服务器并发送
        server = smtplib.SMTP()
        server.connect(self.smtp_server)
        server.login(self.send_user,self.password)
        server.sendmail(user,self.receiver_list,msgRoot.as_string())
        server.close()

    # 邮件内容统计类
    def send_main(self, dict_static_run, dict_static_api):
        '''
        :param
            dict_static_run:  测试概要统计字典
            dict_static_api:  测试接口统计字典
        '''

        sub = "接口自动化测试报告"
        head="""\
<!DOCTYPE html>
<html>
<head>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Load Test Results</title>

</head>
"""
        # 运行统计信息
        body_static="""\
<body style="font:normal 68% verdana,arial,helvetica;color:#000000;">
<h1 style="margin: 0%px 0%px 5%px; font: bold 165% verdana,arial,helvetica">接口测试概览报告</h1>

<table width="100%">
<tr>
<td align="left">Date report: {_end_strftime}</td>
<td align="right">Designed for use with <a href="https://www.jiatui.com/?source=bdpz"> @JiaTui </a>APITester.</td>
</tr>
</table>

<hr size="1">
<h2 style="margin-top: 1em; margin-bottom: 0.5em; font: bold 140% verdana,arial,helvetica">运行概要信息</h2>

<table width="95%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
<tr valign="top">
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">测试开始时间</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">测试结束时间</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">测试总耗时</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">测试接口数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">运行用例数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">通过用例数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">失败用例数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">测试通过率</th>
</tr>
<tr valign="top" class="Failure" style="font-weight:bold;">
    <td align="center" style="background:#eeeee0;white-space: nowrap;">{_start_strftime}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;">{_end_strftime}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;">{_sum_time}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;">{_api_counts}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;">{_cases_count}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;color:green;">{_pass_counts}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;color:red;">{_fail_counts}</td>
    <td align="center" style="background:#eeeee0;white-space: nowrap;color:red;">{_pass_rate}</td>
</tr>
</table>

<hr size="1">
<h2 style="margin-top: 1em; margin-bottom: 0.5em; font: bold 140% verdana,arial,helvetica">运行失败接口统计</h2>

<table width="95%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
<tr valign="top">
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">项目名称</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">接口名称</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">运行用例数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">通过用例数</th>
    <th style="color: #ffffff;font-weight: bold;text-align:center;background:#2674a6;white-space: nowrap;">失败用例数</th>
</tr>
""".format(_start_strftime=dict_static_run['start_strftime'],
            _end_strftime=dict_static_run['end_strftime'],
            _sum_time=dict_static_run['sum_time'],
            _api_counts=dict_static_run['api_counts'],
            _cases_count=dict_static_run['cases_count'],
            _pass_counts=dict_static_run['pass_counts'],
            _fail_counts=dict_static_run['fail_counts'],
            _pass_rate=dict_static_run['pass_rate'],
          )

        # 依次添加失败的接口统计数据
        body_static_api = ""
        fail_apis = []  # 失败的接口集
        fail_projs = []  # 失败的项目集
        dict_static_fail = {}  # 统计所有失败用例的的接口
        end_html = """
</table>
</body>
</html>
"""
        # 统计失败的接口信息
        for k,v in dict_static_api.items():
            if len(v['fail']) > 0:
                fail_apis.append(k)
                fail_projs.append(v['proj'])
                fail_projs=list(set(fail_projs))
                dict_static_fail[k] = v

        # 写入失败的接口信息
        if len(fail_apis) != 0:
            # 按项目排序
            for fail_proj in fail_projs:
                for k, v in dict_static_fail.items():
                    proj_name = dict_static_fail[k]['proj']
                    if proj_name in fail_proj:
                        api_name = k
                        cases_counts = len(dict_static_fail[k]['pass'])+len(dict_static_fail[k]['fail'])
                        pass_counts = len(dict_static_fail[k]['pass'])
                        fail_counts = len(dict_static_fail[k]['fail'])
                        api_html_data = """
    <tr valign="top" class="Failure" style="font-weight:bold; ">
        <td align="center" style="background:#eeeee0;white-space: nowrap;">{_proj_name}</td>
        <td align="center" style="background:#eeeee0;white-space: nowrap;">{_api_name}</td>
        <td align="center" style="background:#eeeee0;white-space: nowrap;">{_cases_counts}</td>
        <td align="center" style="background:#eeeee0;white-space: nowrap;color:green;">{_pass_counts}</td>
        <td align="center" style="background:#eeeee0;white-space: nowrap;color:red;">{_fail_counts}</td>
    </tr>
    """.format(_proj_name=proj_name,
               _api_name=api_name,
               _cases_counts=cases_counts,
               _pass_counts=pass_counts,
               _fail_counts=fail_counts)
                        body_static_api = body_static_api + api_html_data
            body_static_api = body_static_api + end_html
        else:
            # 运行接口统计信息
            body_static_api = """
</table>
</body>
</html>
"""
        content=head + body_static + body_static_api
        self.send_mail(sub,content)

if __name__ == "__main__":
    dict_static_api = {
        'user': {
            'pass': ['mock-01', 'mock-02'],
            'fail': [],
            'proj': "用户中心"
        },
        'mockToken': {
            'pass': ['mock-03'],
            'fail': [],
            'proj': "mock管理中心"
        },
        'login': {
            'pass': ['mock-04', 'mock-05'],
            'fail': ['mock-06', 'mock-07'],
            'proj': "登录中心"
        },
        'testrele': {
            'pass': ['mock-08', 'mock-09'],
            'fail': [],
            'proj': "关联数据中心"
        }
    }
    dict_static_run = {
        'title': '---------------------------运行结果概要统计:----------------------------',
        'start_strftime': '2018-05-31 15_17_09',
        'end_strftime': '2018-05-31 15_17_09',
        'sum_time': '0.07',
        'api_counts': 4,
        'cases_count': 9,
        'pass_counts': 7,
        'fail_counts': 2,
        'pass_rate': '77.78%',
        'fail_cases': ['mock-06', 'mock-07']
    }
    sen = SendEmail()
    sen.send_main(dict_static_run, dict_static_api)
