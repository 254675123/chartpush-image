# -*- coding: utf-8 -*-
# coding=utf-8

import time
import json
import logging
import datetime

from mysql.connector import Error

from config import config
from database import tool
from database.mongodb import Mongodb
from database.mysqldb import Mysqldb
from solr.solr_server import SolrServer
from duplicate_removal import ChartDuplicate
from multiple_thread.thread_manager import ThreadManager
from algorithm.kmeans_wordsize import KmeansWordSize
from chart_builder_items import BuilderChartItems


class ChartPusher(BuilderChartItems):
    """
    推送算法团队识别的图表到索引
    """

    def __init__(self):
        super(ChartPusher,self).__init__()
        self.__sleep_time_per_request = 0.01
        self.__sleep_time_per_request_none = 180.00
        self.__sleep_time_per_loop = 60
        self.__page_size = 1
        self.__total_num = 0
        self.__recovery = True

        self.__word_size = []
        self.thread_manager = ThreadManager(1)
        self.collection = Mongodb.getMongodbCollection('hb_charts')


    @staticmethod
    def start(target):
        pusher = ChartPusher()

        pusher.__dispatchTask(target)

        return pusher.result_list

    def __dispatchTask(self, target):
        # '/niub/www/sourcecode/ResearchReporterTool-2.4-ssd-123/image_ids_isolate'+ str(target)
        logging.info('target:'+str(target))
        image_ids = None
        if target == '0':
            logging.info('read file')
            image_ids = open('image_ids', 'r')
            ids_lines = image_ids.readlines()

        else:
            logging.info('parameter:'+target)
            ids_lines = target.split(',')

        for line in ids_lines:
            id = line.strip('\n')
            id = id.strip('\r')

            logging.info('Start to select data')

            logging.info('the id is :' + str(id))
            chart_items = self.collection.find({'_id': id})

            #chart_items = self.collection.find({'text_info': {'$exists': 1}})

            # print chart_items
            chart_items = self.convertRecordsToArray(chart_items)
            length = len(chart_items)
            logging.info(length)
            logging.info('Finished to select data')
            if length == 0:
                time.sleep(self.__sleep_time_per_request_none)
            else:
                self.thread_manager.run(chart_items, self.__updateThreadFunc, target=target)
                time.sleep(self.__sleep_time_per_request)
        if image_ids is not None:
            image_ids.close()
        logging.info('Done')



    def __updateThreadFunc(self, data, args):
        target = args['target']
        thread_id = args['__thread_id']
        chart_items, id_list = self.buildUpdateItems(data)

        code = self.pushIndex(chart_items, thread_id)
        if code == 200:
            #self.collection.update({'_id': {'$in': id_list}}, {'$set': {'state': target}}, multi=True)
            logging.info("push success.")
        # exception process
        else:
            logging.info("push fail.")

        logging.info('push index,code:' + str(code))
        self.result_list.append(id_list[0] + ':' + str(code))



