* 框架简介：jtApiTest ，基于python3+requests+unnittest+yaml+ddt封装的接口自动化测试框架

* 最新版本与修改
    - # v0.5
        - 1.新增单个接口过滤的skip -- ok
        - 2.修改Beautiful源码，调整报告输出增加请求体、响应体、caseid、case_desc等详细信息
        - 3.用例运行响应时间精确到ms -- ok
        - 4.简化yaml，抽取case公共数据 -- ok
        - 5.优化日志输出格式 -- ok
        - 6.yaml增加skip过滤单个用例功能
        - 7.调整关联逻辑.

    - # v0.1
        - 1.构建框架基本结构 python+requests+unittest+yaml+ddt.
        - 2.完成demo用例输出.

* 框架特色
    - 灵活配置：支持以配置文件的方式管理配置，如日志配置与email配置等
    - 报告记录：测试结果报告记录丰富，包含 测试概览报告 与 测试详细报告 等，简单易读
    - 邮件支持：支持基于smtp的方式发送email
    - 兼容性强：基于requests模块进行测试，并集成yaml与ddt进行数据驱动
    - 扩展性强：基于python3开发，方便后续对框架功能的扩展

* 目录结构
    - /conf         ： 配置文件目录，包含构建配置、邮件配置、日志配置等
    - /data         ： 数据文件目录，包括用例数据管理文件夹caseData、公共数据管理文件夹pubData等
    - /log          ： 运行时日志目录
    - /report       ： 测试报告目录
    - /src          ： 源码管理目录，包含基础类、工具类、公共类、用例类等
    - start.py      ： 框架执行入口
    - README.MD     ： 框架简介

* 运行环境
    - python3.6+

* 运行依赖
    - unittest
    - requests 2.18.4+
    - pyyaml 3.13+
    - jsonpath_rw 1.4.0+
    - ddt 1.2.0+
    - configparser
    - BeautifulReport

* 用例demo
    -   # 被需要关联数据的用例demo
      case_id: get_guest_1
      desc: "查询成功"
      skip: 1       # skip值为1表示跳过该用例执行
      request:
          url: http://192.168.102.111:8000/api/get_guest_list
          method: GET
          header:
              Accept: application/json, text/javascript, */*; q=0.01
          data:
              eid: 5
      relyDataExport: # 关联输出，即该接口响应返回被其他接口关联字段
          - {"relyKey": "phone", "keepKey": "MyPhone"}
      validators:           # 断言设置
          - {"check": "status", "expect": 200}


    -    # 需要关联数据的用例demo
      case_id: get_guest_4      # 用例编号
      desc: "eid为空查询phone"   # 用例描述
      request:                  # 请求内容
          url: http://192.168.102.111:8000/api/get_guest_list
          method: GET
          header:
              Accept: application/json, text/javascript, */*; q=0.01
          data:                 # 测试模块
              phone: 13700000004
      validators:               # 断言设置
          - {"check": "status", "expect": 10021}
          - {"check": "message", "expect": "eid cannot be empty"}
      relyDataImport:  # 关联引入，即该接口运行所需的关联字段设置
          - {"relyDataSrc": "phone", "relyDataDes": "phone"}  # relyDataSrc：需要关联数据的字段,relyDataDes：需要替换数据的字段
          - {"relyDataSrc": "phone", "relyDataDes": "phone2"}
