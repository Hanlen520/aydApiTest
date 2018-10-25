* 框架简介：jtApiTest ，基于python3+requests+unnittest+yaml+ddt封装的接口自动化测试框架

* 框架特色
    - 灵活配置：支持以配置文件的方式管理配置，如日志配置与email配置等
    - 报告记录：测试结果报告记录丰富，包含 测试概览报告 与 测试详细报告 等，简单易读
    - 邮件支持：支持基于smtp的方式发送email
    - 兼容性强：基于requests模块进行测试，并集成yaml与ddt进行数据驱动
    - 扩展性强：基于python3开发，方便后续对框架功能的扩展

* 目录结构
    /conf         ： 配置文件目录，包含构建配置、邮件配置、日志配置等
    /data         ： 数据文件目录，包括用例数据管理文件夹caseData、公共数据管理文件夹pubData等
    /log          ： 运行时日志目录
    /report       ： 测试报告目录
    /src          ： 源码管理目录，包含基础类、工具类、公共类、用例类等
    start.py      ： 框架执行入口
    README.MD     ： 框架简介

* 运行环境
    python3.6+

* 运行依赖
    unittest
    requests 2.18.4+
    pyyaml 3.13+
    jsonpath_rw 1.4.0+
    ddt 1.2.0+
    configparser
    BeautifulReport

* 用例demo
-   # 被需要关联数据的用例
  case_id: get_guest_1
  desc: "查询成功"
  module: "用户模块"
  request:
      url: http://192.168.102.111:8000/api/get_guest_list
      method: GET
      header:
          Accept: application/json, text/javascript, */*; q=0.01
      data:
          eid: 5
  relyDataKey: "phone"  # 被关联数据在响应中的字段名
  validators:
      - {"check": "status", "expect": 200}


-    # 需要关联数据的用例
  case_id: get_guest_4      # 用例编号
  desc: "eid为空查询phone"
  module: "用户模块"
  request:                  # 用例描述
      url: http://192.168.102.111:8000/api/get_guest_list
      method: GET
      header:
          Accept: application/json, text/javascript, */*; q=0.01
      data:                 # 测试模块
          phone: 13700000004
  validators:               # 请求内容
      - {"check": "status", "expect": 10021}
      - {"check": "message", "expect": "eid cannot be empty"}
  relyDataVal:              # 如果有关联数据，写在这里
      - {"relyDataSrc": "phone", "relyDataDes": "phone"}  # relyDataSrc：需要关联数据的字段,relyDataDes：需要替换数据的字段
      - {"relyDataSrc": "phone", "relyDataDes": "phone2"}