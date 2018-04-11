# -*- coding: utf-8 -*-
# coding=utf-8

import time
import os
import logging
import sys

import datetime
from mysql.connector import Error

from database.mongodb import Mongodb
from database.mysqldb import Mysqldb

from multiple_thread.thread_manager import ThreadManager


class ChartState:
    def __init__(self):
        pass

    INVALID = -1
    UNSYNCED = 0
    SYNCED = 1
    UPDATED = 2
    DELETED = 3
    DEPRECATED = 4
    DEPRECATED_NEW = 5
    SYNCED_NEW = 6

class UpdateDictionary:
    """
    推送算法团队识别的图表到索引
    """

    def __init__(self):
        self.__sleep_time_one_hour = 3600.00
        self.__old_list = []
        self.__new_list = []

        reload(sys)
        sys.setdefaultencoding('utf-8')

    @staticmethod
    def start(args):
        pusher = UpdateDictionary()
        pusher.__dispatchTask(args)

    def __dispatchTask(self, args):
        self.__target = args.target
        self.__usedate = args.usedate

        logging.info('target:'+str(self.__target))
        logging.info('usedate:' + str(self.__usedate))


        while True:
            logging.info('Start to select data')

            # 获取当前时间
            curtime = datetime.datetime.now()

            # 仅在凌晨2点才会更新同义词
            if curtime.hour == 17:

                # 1. read old file for old data
                self.__readFile()
                self.__readStockFile()

                # 2. read mysql for new data
                # get syn data
                sql = "select dict_word,synonym from dict_synonyms"
                rows = self.__getMysqlData(sql)
                self.__getSynDict(rows)

                # 3. merge old data and new data to file
                self.__writeFile()

                # 4. execute sh script to update the file to zookeeper
                #self.__executeShell()


                logging.info('update data over.')

                time.sleep(self.__sleep_time_one_hour)

            else:
                time.sleep(self.__sleep_time_one_hour)



        logging.info('Done')



    # read old file for old data
    def __readFile(self):
        ""

        logging.info('start read old file.')

        # 1. open file
        # 使用open打开文件后一定要记得调用文件对象的close()方法。比如可以用try/finally语句来确保最后能关闭文件。
        # 注：不能把open语句放在try块里，因为当打开文件出现异常时，文件对象file_object无法执行close()方法。
        #fin = open('/usr/local/solrcloud/solrconfig-6.6.0/synonyms-base.txt')
        fin = open('/home/lchzhang/temp/synonyms-base.txt')

        # 2. read file
        # 如果文件是文本文件，还可以直接遍历文件对象获取每行
        try:
            self.__old_list = []
            lines = fin.readlines()
            for line in lines:
                self.__old_list.append(line)
        finally:
            fin.close()

    # read stock file for old data
    def __readStockFile(self):
        ""

        logging.info('start read stock file.')

        # 1. open file
        # 使用open打开文件后一定要记得调用文件对象的close()方法。比如可以用try/finally语句来确保最后能关闭文件。
        # 注：不能把open语句放在try块里，因为当打开文件出现异常时，文件对象file_object无法执行close()方法。
        #fin = open('/usr/local/solrcloud/solrconfig-6.6.0/synonyms-base.txt')
        fin = open('/home/lchzhang/stock-11')

        # 2. read file
        # 如果文件是文本文件，还可以直接遍历文件对象获取每行
        try:
            lines = fin.readlines()
            for line in lines:
                if line.endswith(',\r\n'):
                    continue
                self.__old_list.append(line)
        finally:
            fin.close()


    def __getMysqlData(self, sql):
        mysql = Mysqldb.getMysqlInstance()
        cursor = mysql.cursor()
        rows = None
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            #if rows is not None:
            #    rows = tool.convertRowToKeyValue(cursor, rows)
        except Error as error:
            logging.error('Failed to find record, error:{}'.format(error))

        finally:
            cursor.close()

        mysql.close()
        return rows


    def __getSynDict(self, rows):
        "生成同义词数组"

        # clear data
        self.__new_list = []
        self.__new_list.append('\r\n')
        for syn in rows:
            if syn[0] is None or syn[1] is None:
                continue
            key = syn[1].encode('utf-8')

            if key.find(' ') > 0 or key.find(',') > 0 or key.find('有限') > 0 or key == '无':
                continue
            if key.find('(') > 0 or key.find('（') > 0 or key.find('.') > 0 or key.find('-') > 0 or key.find('+') > 0:
                continue
            if key.find('、') > 0 or key.find('/') > 0:
                continue
            val = syn[0].encode('utf-8')
            if val.find(' ') > 0 or val.find(',') > 0 or val.find('有限') > 0:
                continue
            self.__new_list.append(key + ' => ' + key + ',' + val + '\r\n')




    def __writeFile(self):
        logging.info('start write mysynonyms file.')
        fin = open('/home/lchzhang/temp/mysynonyms.txt', 'w')
        try:
            fin.writelines(self.__old_list)
            fin.writelines(self.__new_list)
            fin.flush()
        except Error as error:
            logging.error('Failed to write synonyms word, error:{}'.format(error))
        finally:
            fin.close()



    def __executeShell(self):
        "execute shell script"

        res = os.popen('/usr/local/solrcloud/online.sh')
        lines = res.readlines()
        print lines




