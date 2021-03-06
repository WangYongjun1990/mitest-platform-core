# encoding: utf-8

"""
Built-in dependent functions used in YAML/JSON testcases.
"""

import datetime
import json
import os
import random
import re
import string
import time

from mitest.api.mysql_sql_executor import sql_execute
from mitest.httprunner.compat import basestring, builtin_str, integer_types, str
from mitest.httprunner.exception import ParamsError
from mitest.utils.encryption import Encryption
from mitest.utils.tools import is_json_contains
from requests_toolbelt import MultipartEncoder
from mitest.utils.custom import *


""" built-in functions
"""
def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))

def get_timestamp(str_len=13):
    """ get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, integer_types) and 0 < str_len < 17:
        return builtin_str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")

def get_current_date(fmt="%Y-%m-%d"):
    """ get current date, default format is %Y-%m-%d
    """
    return datetime.datetime.now().strftime(fmt)

def multipart_encoder(field_name, file_path, file_type=None, file_headers=None):
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)

    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        fields = {
            field_name: (filename, f.read(), file_type)
        }

    return MultipartEncoder(fields)

def multipart_content_type(multipart_encoder):
    return multipart_encoder.content_type


""" built-in comparators
"""
def equals(check_value, expect_value):
    assert check_value == expect_value

def less_than(check_value, expect_value):
    assert check_value < expect_value

def less_than_or_equals(check_value, expect_value):
    assert check_value <= expect_value

def greater_than(check_value, expect_value):
    assert check_value > expect_value

def greater_than_or_equals(check_value, expect_value):
    assert check_value >= expect_value

def not_equals(check_value, expect_value):
    assert check_value != expect_value

def string_equals(check_value, expect_value):
    assert builtin_str(check_value) == builtin_str(expect_value)

def length_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) == expect_value

def length_greater_than(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) > expect_value

def length_greater_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) >= expect_value

def length_less_than(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) < expect_value

def length_less_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) <= expect_value

def contains(check_value, expect_value):
    assert isinstance(check_value, (list, tuple, dict, basestring))
    assert expect_value in check_value

def contained_by(check_value, expect_value):
    assert isinstance(expect_value, (list, tuple, dict, basestring))
    assert check_value in expect_value

def type_match(check_value, expect_value):
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, basestring):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    assert isinstance(check_value, get_type(expect_value))

def regex_match(check_value, expect_value):
    assert isinstance(expect_value, basestring)
    assert isinstance(check_value, basestring)
    assert re.match(expect_value, check_value)

def startswith(check_value, expect_value):
    assert builtin_str(check_value).startswith(builtin_str(expect_value))

def endswith(check_value, expect_value):
    assert builtin_str(check_value).endswith(builtin_str(expect_value))


# def json_contains(check_value, expect_value):
#     assert isinstance(check_value, basestring)
#     # bytes转str
#     str_content = check_value.decode('utf-8')
#     # str转dict
#     dict_check = json.loads(str_content)
#     assert isinstance(expect_value, basestring)
#     dict_expect = json.loads(expect_value)
#     # for key in dict_expect:
#     #     assert key in dict_check
#     #     assert dict_check[key] == dict_expect[key]
#     assert is_json_contains(dict_check, dict_expect)




""" built-in hooks
"""
def setup_hook_prepare_kwargs(request):
    if request["method"] == "POST":
        content_type = request.get("headers", {}).get("content-type")
        if content_type and "data" in request:
            # if request content-type is application/json, request data should be dumped
            if content_type.startswith("application/json") and isinstance(request["data"], (dict, list)):
                request["data"] = json.dumps(request["data"])

            if isinstance(request["data"], str):
                request["data"] = request["data"].encode('utf-8')

def sleep_N_secs(n_secs):
    """ sleep n seconds
    """
    time.sleep(n_secs)


# def teardown_db_select(response, sql=None):
#     # bytes转str
#     str_content = response.content.decode('utf-8')
#     # str转dict
#     dict_content = json.loads(str_content)
#     # 添加sql查询结果
#     dict_content['db_result'] = sql
#     # dict转str_json
#     str_content = json.dumps(dict_content, ensure_ascii=False)
#     # str_json转bytes
#     response.content = str_content.encode('utf-8')
#
#
# def db_select(sql):
#     return sql + 's'


# def add_sign(request):
#     e = Encryption()
#     if 'json' in request:
#         request['json'] = json.loads(e.map_to_sign_common(request['json']))
