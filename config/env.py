# -*- coding: utf-8 -*-
# coding=utf-8

# const env type
ENV_PROD = 'ENV_PROD'
ENV_TEST = 'ENV_TEST'
ENV_DICT = 'ENV_DICT'
ENV_CICC = 'ENV_CICC'
ENV_EXCEL = 'ENV_EXCEL'
ENV_DEV = 'ENV_DEV'

# global env 
runtime_env = None


# get current environment
def getEnv():
    """ ENV_PROD ENV_TEST ENV_DEV """
    global runtime_env

    if runtime_env is not None:
        return runtime_env

    env_file = open('env', 'r')
    runtime_env = env_file.readline().strip('\n')
    env_file.close()

    if runtime_env == '':
        runtime_env = ENV_DEV

    return runtime_env
