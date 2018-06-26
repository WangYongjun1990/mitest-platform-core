# -*- coding:utf-8 -*-

"""
File Name: `run_test`.py
Version:
Description:

Author: wangyongjun
Date: 2018/6/22 下午9:49
"""
import time

from httprunner import HttpRunner
from mitest.engine.exceptions import RunCaseError, LoadCaseError
from mitest.engine.load_test import load_test


def run_test(**kwargs):
    testset = load_test(**kwargs)

    if not testset:
        raise LoadCaseError('没有可执行的用例')

    print("testset:{0}\n{1}".format(testset, type(testset)))
    try:
        summary = run(testset, report_name='testMock')
    except Exception:
        raise RunCaseError
    print(summary)


def run(testset_path, report_name='default'):
    """
    用例运行
    :param testset_path: dict or list
    :param report_name: str
    :return:
    """
    kwargs = {
        "failfast": False,
    }
    runner = HttpRunner(**kwargs)
    start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    runner.run(testset_path)
    runner.gen_html_report(
        html_report_name=report_name,
        # html_report_template="/path/to/custom_report_template"
    )
    return runner.summary

if __name__ == '__main__':
    kwargs = {
        # "testcase_id_list": ['1', '2', '3'],
        "env_name": "mock",
        # "testsuite_id_list": ['1'],
        "module_id_list": ['4'],
    }
    run_test(**kwargs)
    # run_test(testcase_id='1', env_name='mo2ck')
    testset = {
            "name": "myMock",
            "config": {
                "request": {
                    "base_url": "http://99.48.58.241",
                    "headers": {
                        "Content-Type": "application/json;charset=UTF-8"
                    }
                },
                "variables": [
                    {"pageSize": 1},
                    {"currentPage": 1}
                ],
                "parameters": [],
                "name": "testset description"
            },
            "testcases": [
                {
                    "request": {
                        "json": {},
                        "url": "mock/config/queryProject",
                        "headers": {"Content-Type": "application/json"},
                        "method": "POST"
                    },
                    "extract": [
                        {
                            "op": "content.desc.ups.0"
                        }
                    ],
                    "validate": [
                        {
                            "eq": [
                                "status_code",
                                200
                            ]
                        },
                        {
                            "eq": [
                                "headers.Content-Type",
                                "application/json"
                            ]
                        },
                        {
                            "eq": [
                                "content.desc",
                                {"bds": [], "capital": ["businessapi/ops/file/upload/2/xydadcce31a92e8b1c5",
                                                        "mm/credit/getUnderWrittingStatus",
                                                        "mm/credit/getUnderWrittingStatus/2/xydadcce31a92e8b1c5",
                                                        "mm/credit/queryAccountInfo",
                                                        "mm/credit/queryAccountInfo/2/xydadcce31a92e8b1c5",
                                                        "mm/credit/saveUserInfo/2/xydadcce31a92e8b1c5",
                                                        "mm/credit/withdrawDeposit/2"],
                                 "ups": ["demo_get", "demo_post", "demo_post_form", "demo_post_json"]}
                            ]
                        }
                    ],
                    "variables": [],
                    "name": "queryProject"
                },
                {
                    "request": {
                        "json": {
                            "pageSize": "$pageSize",
                            "interfaceName": "demo_post_json",
                            "currentPage": "$currentPage",
                            "projectName": "ups",
                            "op": "$op"
                        },
                        "url": "http://99.48.58.241/mock/config/queryMock",
                        "headers": {},
                        "method": "POST"
                    },
                    "extract": [
                        {
                            "tableData": "content.tableData"
                        }
                    ],
                    "validate": [
                        {
                            "eq": [
                                "status_code",
                                200
                            ]
                        },
                        {
                            "eq": [
                                "headers.Content-Type",
                                "application/json"
                            ]
                        },
                        {
                            "eq": [
                                "content.code",
                                "000"
                            ]
                        }
                    ],
                    "variables": [],
                    "name": "queryMock"
                }
            ]
        }

    # run_test(testset, 'myReport')
