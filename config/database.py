# -*- coding: utf-8 -*-
# coding=utf-8

import env


# get mysql config
def getMysqlConfig():
    runtime_env = env.getEnv()
    if runtime_env == env.ENV_PROD:
        return {
            'MYSQL_DATABASE': 'core_doc',
            'MYSQL_HOST': '10.117.211.16',
            'MYSQL_PORT': 6033,
            'MYSQL_USER': 'core_bj',
            'MYSQL_PASSWORD': 'alUXKHIrJoAOuI26'
        }
    elif runtime_env == env.ENV_TEST:
        return {
            'MYSQL_DATABASE': 'db_cicc_portal',
            'MYSQL_HOST': '10.11.255.56',
            'MYSQL_PORT': 3306,
            'MYSQL_USER': 'root',
            'MYSQL_PASSWORD': 'abcft'
        }
    elif runtime_env == env.ENV_DICT:
        return {
            'MYSQL_DATABASE': 'search_word',
            'MYSQL_HOST': '114.55.108.136',
            'MYSQL_PORT': 3306,
            'MYSQL_USER': 'team_bj',
            'MYSQL_PASSWORD': 'P9WdpTHVoX17eWPK'
        }
    elif runtime_env == env.ENV_CICC:
        return {
            'MYSQL_DATABASE': 'db_cicc_portal',
            'MYSQL_HOST': '192.168.1.241',
            'MYSQL_PORT': 3306,
            'MYSQL_USER': 'bj_cicc_portal',
            'MYSQL_PASSWORD': 'dc81167f409d'
        }
    else:
        return {
            'MYSQL_DATABASE': 'r_reportor',
            'MYSQL_HOST': '10.11.255.110',
            'MYSQL_PORT': 31306,
            'MYSQL_USER': 'rreportor',
            'MYSQL_PASSWORD': 'saWQR432QR'
        }


# get mongodb config
def getMongodbConfig():
    runtime_env = env.getEnv()
    if runtime_env == env.ENV_PROD:
        return {
            # hk cluster
            #'MONGO_URI': 'mongodb://hk_soutu:188e1af79e7a@dds-j6cd3f25db6afa741.mongodb.rds.aliyuncs.com:3717,dds-j6cd3f25db6afa742.mongodb.rds.aliyuncs.com:3717/cr_data',
            # online cluster
            'MONGO_URI': 'mongodb://search:ba3Re3ame%2bWa@dds-bp1d09d4b278ceb42.mongodb.rds.aliyuncs.com:3717,dds-bp1d09d4b278ceb41.mongodb.rds.aliyuncs.com:3717/cr_data',
            # online service 009
            #'MONGO_URI': 'mongodb://bj_alg_collection:5284f31f4ef9@dds-bp1d09d4b278ceb41.mongodb.rds.aliyuncs.com:3717/cr_data',
            # online service 008
            #'MONGO_URI': 'mongodb://algorithm:8ebpZw7ZSRvZ@10.81.75.17:27017/cr_data',
            # online service 007
            #'MONGO_URI': 'mongodb://algorithm:keoOIRNCWan6@10.24.254.27:27017/cr_data',
            # email offline
            #'MONGO_URI': 'mongodb://chlzhang:8d364706055c@121.43.60.53:8703/wechatReading',
            #'MONGO_URI': 'mongodb://modeling_user:LKJHGFDSA@10.24.254.29:27017/wechatReading',
            # email pre
            #'MONGO_URI': 'mongodb://bj_wechatRead:90afba1128da@10.168.46.10:3017/wechatReading',
            # email online prod
            #'MONGO_URI': 'mongodb://10.168.30.235:3017/wechatReading',
            #'MONGO_DATABASE': 'wechatReading'
            'MONGO_DATABASE': 'cr_data'
        }
    elif runtime_env == env.ENV_TEST:
        return {
            'MONGO_URI': 'mongodb://search:IiTZ1t7GiCB7@119.3.6.152:3717/cr_data',
            'MONGO_DATABASE': 'cr_data'
        }
    elif runtime_env == env.ENV_DICT:
        return {
            'MONGO_URI': 'mongodb://algorithm:cH7jufath5_a@120.26.13.228:3717/cr_data',
            'MONGO_DATABASE': 'cr_data'
        }
    elif runtime_env == env.ENV_CICC:
        return {
            'MONGO_URI': 'mongodb://search:IiTZ1t7GiCB7@192.168.1.204:3717/cr_data',
            'MONGO_DATABASE': 'cr_data'
        }
    elif runtime_env == env.ENV_EXCEL:
        return {
            'MONGO_URI': 'mongodb://algorithm:keoOIRNCWan6@114.55.73.185:27017/cr_data',
            'MONGO_DATABASE': 'cr_data'
        }
    else:
        return {
            'MONGO_URI': 'mongodb://search:ba3Re3ame%2bWa@121.40.131.65:3718/cr_data',
            'MONGO_DATABASE': 'cr_data'
        }
