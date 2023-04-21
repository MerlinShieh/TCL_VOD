# -*- coding:utf-8 -*-
# @Time    : 2023/4/05
# @Author  : Merlin
# @File    : _log.py
# *************************

import os
import sys
from loguru import logger as log
from functools import wraps


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
LOG_DIR = os.path.join(BASE_DIR, 'log')
file_stream = False
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print(LOG_DIR, '路径已存在')
    file_stream = True
LOG_DIR = os.path.join(LOG_DIR, 'VOD_{time}.log')
log.add(LOG_DIR, rotation='50 MB', level="DEBUG")


def logger(param):
    def wrap(function):
        @wraps(function)
        def _wrap(*args, **kwargs):
            log.info("当前模块 {}".format(param))
            log.info("全部args参数参数信息 , {}".format(str(args)))
            log.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            result = function(*args, **kwargs)
            log.debug("当前函数执行结果 , {}".format(result))
            return result
        return _wrap
    return wrap


if __name__ == '__main__':
    log.info('这是一个测试日志')