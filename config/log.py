# -*- coding: utf-8 -*-
# coding=utf-8
# 
from os import makedirs
from os import path
from os.path import join

import logging


# init log basic config
def initLogConfig():
    log_path = './log/'
    if not path.isdir(log_path):
        makedirs(log_path)

    logging.basicConfig(
        level=logging.INFO,
        filename=join(log_path, 'service.log'),
        format='%(asctime)s[%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    #logging._handlers.RotatingFileHandler(join(log_path, 'service.log'), maxBytes=1024 * 1024, backupCount=10)
