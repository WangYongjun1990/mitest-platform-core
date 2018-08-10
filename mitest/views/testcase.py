# -*- coding:utf-8 -*-

"""
File Name: `testcase`.py
Version:
Description:

Author: wangyongjun
Date: 2018/6/21 13:44
"""
import json

from flask import Blueprint
from flask_restful import Resource

from mitest.api.comm_log import logger
from mitest.engine.handle_testcase import handle_testcase
from mitest.views.wrappers import timer
from mitest.utils.common import get_request_json, make_response

testcase = Blueprint('testcase_interface', __name__)


class Testcase(Resource):
    def __init__(self):
        pass

    @timer
    def post(self, action):
        data = get_request_json()

        if action == 'add':
            handle_testcase(action, **data)

        elif action == 'edit':
            pass

        elif action == 'delete':
            pass

        elif action == 'detail':
            pass

        elif action == 'list':
            pass

        else:
            return make_response({"code": "100", "desc": "url错误，不存在的接口动作<{action}>".format(action=action)})