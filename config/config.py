# -*- coding: utf-8 -*-
# coding=utf-8

import log
import env


# init config
def init():
    log.initLogConfig()


# get mongodb config
def getChartSolrAPI():
    runtime_env = env.getEnv()
    if runtime_env == env.ENV_PROD:
        return {
            'SOLR_CHAT_UPDATE_356': ('http://10.168.123.53:8080/solrweb/chartIndexByUpdate',
                                     'http://10.168.117.133:8080/solrweb/chartIndexByUpdate',
                                     'http://10.51.7.161:8080/solrweb/chartIndexByUpdate',),

            'SOLR_CHAT_UPDATE_789': ('http://10.252.214.227:8080/solrweb/chartIndexByUpdate',
                                     'http://10.252.218.226:8080/solrweb/chartIndexByUpdate',
                                     'http://10.117.10.24:8080/solrweb/chartIndexByUpdate',),

            'SOLR_CHAT_UPDATE_SSD_123': ('http://10.24.235.70:8080/solrweb/chartIndexByUpdate',
                                         'http://10.24.234.190:8080/solrweb/chartIndexByUpdate',
                                         'http://10.24.235.15:8080/solrweb/chartIndexByUpdate',),

            'SOLR_CHAT_UPDATE_SSD_456': ('http://10.24.254.66:8080/solrweb/chartIndexByUpdate',
                                         'http://10.24.254.107:8080/solrweb/chartIndexByUpdate',
                                         'http://10.24.155.54:8080/solrweb/chartIndexByUpdate',),
            'HK_CHAT_UPDATE_SSD_123': ('http://172.31.223.179:8080/solrweb/chartIndexByUpdate',
                                       'http://172.31.223.180:8080/solrweb/chartIndexByUpdate',
                                       'http://172.31.223.181:8080/solrweb/chartIndexByUpdate',),

            'SOLR_CHAT_UPDATE_2': ('http://10.168.20.246:8080/solrweb/chartIndexByUpdate?origin_from=chart',),

            'SOLR_CHAT_UPDATE_3': ('http://10.168.123.53:8080/solrweb/chartIndexByUpdate',),

            'SOLR_CHAT_UPDATE_7': ('http://10.252.214.227:8080/solrweb/chartIndexByUpdate?single=true',),
            'SOLR_CHAT_UPDATE_8': ('http://10.252.218.226:8080/solrweb/chartIndexByUpdate?single=true',),
            'SOLR_CHAT_UPDATE_9': ('http://10.117.10.24:8080/solrweb/chartIndexByUpdate?single=true',),


            'SOLR_CHAT_DELETE_8': ('http://10.252.218.226:8080/solrweb/chartIndexByDel',),
            'SOLR_CHAT_UPDATE_PART_SSD_1': ('http://10.24.235.70:8080/solrweb/indexByUpdatePart',),
            'SOLR_CHAT_UPDATE_PART_SSD_4': ('http://10.24.254.66:8080/solrweb/indexByUpdatePart',),
            'SOLR_EMAIL_UPDATE_SSD_1': ('http://10.26.95.47:8080/solrweb/indexByUpdate?single=true&core_name=core_email',),
            'SOLR_EMAIL_UPDATE_SSD_2': ('http://10.25.1.62:8080/solrweb/indexByUpdate?single=true&core_name=core_email',),
            'SOLR_EMAIL_UPDATE_SSD_3': ('http://10.27.0.98:8080/solrweb/indexByUpdate?single=true&core_name=core_email',),
        }
    elif runtime_env == env.ENV_TEST:
        return {
            'SOLR_CHAT_UPDATE': '',
        }
    else:
        return {
            'SOLR_CHAT_UPDATE': ('http://10.12.0.84:8080/solrweb/chartIndexByUpdate?origin_from=chart&local=true',),

            'SOLR_CHAT_DELETE': ('http://10.12.0.84:8080/solrweb/chartIndexByDel?origin_from=chart&local=true',),
        }
