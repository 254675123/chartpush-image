# -*- coding: utf-8 -*-
# coding=utf-8
import time
import json
import logging
from date_encoder import DateEncoder
from mysql.connector import Error
from database import tool
from config import config
from solr.solr_server import SolrServer
from database.mysqldb import Mysqldb
from algorithm.kmeans_wordsize import KmeansWordSize
from duplicate_removal import ChartDuplicate

class BuilderChartItems(object):
    "generate data"


    def __init__(self):
        self.__target = 0
        self.remove_data = False
        self.__id_list = []
        self.__tempfile = {}
        self._chart_duplicate = ChartDuplicate()
        self.result_list = []

    def writeFile(self):
        if len(self.__id_list) == 0:
            return
        logging.info('start write image_ids_isolate file.')
        fin = open('image_ids_isolate'+str(self.__target), 'w+')
        fin.writelines(self.__id_list)
        fin.flush()
        fin.close()
        self.__id_list = []

    def writeFile4error(self,chart_items):
        logging.info('start write error_item file.')
        fin = open('error_item_'+str(self.__target), 'w+')
        res = json.dumps(chart_items,ensure_ascii=False)
        logging.info(res)
        fin.write(res)
        fin.flush()
        fin.close()

    def readFile1(self):
        image_ids = open('image_ids_part', 'r')
        # image_ids = open('image_ids', 'r')
        ids_lines = image_ids.readlines()
        for line in ids_lines:
            arr = line.split(',')
            self.__tempfile[arr[0]] = arr


    def buildUpdateItems(self, chart_items):
        logging.info('Start __buildUpdateItems')
        mysql = Mysqldb.getMysqlInstance()
        files = {}
        data = []
        id_list = []
        #self.readFile1()
        for chart_item in chart_items:

            item = {}
            item['language'] = 1
            item['file_id'] = '' if chart_item['fileId'] is None else str(chart_item['fileId'])
            item['image_id'] = '' if chart_item['_id'] is None else chart_item['_id']
            id_list.append(item['image_id'])
            item['id'] = item['image_id'] + '_' + str(item['language'])
            image_title = '' if 'title' not in chart_item or chart_item['title'] is None else chart_item['title']
            if isinstance(image_title,list):
                continue
            image_title = image_title.strip()
            if image_title == '':
                continue
            else:
                item['image_title'] = image_title
            item['image_url'] = '' if 'svgFile' not in chart_item or chart_item['svgFile'] is None else chart_item['svgFile']
            if len(item['image_url']) == 0:
                item['image_url'] = '' if 'pngFile' not in chart_item or chart_item['pngFile'] is None else chart_item['pngFile']

            #item['chart_type'] = '' if 'chartType' not in chart_item or chart_item['chartType'] is None else chart_item['chartType']
            charttype = '' if 'chartType' not in chart_item or chart_item['chartType'] is None else chart_item[
                'chartType']
            item['chart_type'] = charttype

            bitmaptype = '' if 'bitmap_type' not in chart_item or chart_item['bitmap_type'] is None else chart_item[
                'bitmap_type']
            item['bitmap_type'] = bitmaptype

            if 'doc_score' not in chart_item or chart_item['doc_score'] is None:
                if str(charttype).upper() == 'OTHER' or str(bitmaptype).upper() == 'OTHER':
                    item['doc_score'] = 0.0001
                else:
                    item['doc_score'] = 1.0
            else:
                item['doc_score'] = chart_item['doc_score']

            if self.remove_data or 'data' not in chart_item or chart_item['data'] is None:
                item['chart_data'] = ''
                #logging.info('image_id:' + item['image_id'])
            else :
                item['chart_data'] = json.dumps(chart_item['data'])
                data_length = len(item['chart_data'])
                if data_length >= 100000:
                    item['chart_data'] = ''

            file_data = None
            if self.remove_data or 'file_data' not in chart_item or chart_item['file_data'] is None:
                item['file_data'] = ''
                #logging.info('image_id:' + item['image_id'])
            else :
                item['file_data'] = json.dumps(chart_item['file_data'], cls=DateEncoder)
                file_data = chart_item['file_data']
                data_length = len(item['file_data'])
                if data_length >= 100000:
                    item['file_data'] = ''

            if file_data is not None and isinstance(file_data, dict):
                item['owner_id'] = file_data['user_id']
                item['owner_type'] = 'person'
                item['source_type'] = file_data['collect_source']
                item['source_name'] = file_data['name']
    
            item['source_url'] = '' if 'fileUrl' not in chart_item or chart_item['fileUrl'] is None else chart_item['fileUrl']

            item['chart_version'] = '' if chart_item['chart_version'] is None else chart_item['chart_version']

            if 'text_info' not in chart_item or chart_item['text_info'] is None:
                item['word_imp_level_1'] = ''
                item['word_imp_level_2'] = ''
                item['word_imp_level_3'] = ''
            else:
                kws = KmeansWordSize()
                kws.cluster(item, chart_item)

            #if len(item['chart_data']) >= 32766 or item['chart_type'] == 'BITMAP_CHART':
            #    item['chart_data'] = ''

            # 2017-08-01 texts field for summary by chaolin.zhang
            summary = ''
            if 'texts' not in chart_item or chart_item['texts'] is None:
                item['summary'] = summary
            else:
                for text in chart_item['texts']:
                    if(isinstance(text, dict)) or isinstance(text, list):
                        summary += text['text'] + ','
                    elif(isinstance(text, str)):
                        summary += text + ','
                item['summary'] = summary
                # 如果标题笔记短,summary不太长,用summary代替title
                if len(image_title) <=7 and len(summary) > 0 and len(summary) < 50 and summary.find(image_title) > 0:
                    item['image_title'] = summary

            #item['summary'] = '' if 'texts' not in chart_item or  chart_item['texts'] is None else chart_item['texts']

            # confidence
            if 'confidence' not in chart_item or chart_item['confidence'] is None:
                item['confidence'] = 1.0
            else:
                item['confidence'] = float(chart_item['confidence'])

            legends = []
            if 'legends' not in chart_item or chart_item['legends'] is None:
                item['image_legends'] = ''
            else:
                for legend in chart_item['legends']:
                    legends.append(legend['text'])
                #item['image_legends'] = json.dumps(legends)
                try:
                    item['image_legends'] = ','.join(item for item in legends if item not in [None])
                except Exception as err:
                    print  err
                    print item['image_id']

            #record = None
            file_id = item['file_id']
            if files.has_key(file_id):
                record = files.get(file_id)
            else:
                # 个人搜图不需要关联文件信息
                record = None if chart_item['fileId'] is None else self.getReportItemBySrcId(file_id)
                files[file_id] = record

            if record is not None:
                item['title'] = '' if record['title'] is None else record['title']
                # item['summary'] = '' if record['summary'] is None else record['summary']
                if 'stockcode' in record and record['stockcode'] != '':
                    item['stockcode'] = record['stockcode']
                    item['company'] = '' if record['stockname'] is None else record['stockname']
                else:
                    item['company'] = ''
                    item['stockcode'] = ''

                item['type'] = '' if record['typetitle'] is None else record['typetitle']
                #if str(item['type']).startswith('外文'):
                source = '' if 'source' not in record or record['source'] is None else record['source']
                item['source_name'] = source
                if source == 'tomson':
                    item['language'] = 2
                    item['id'] = item['image_id'] + '_' + str(item['language'])

                origin_time = record['time']
                origin_time_tuple = origin_time.utctimetuple()
                item['year'] = origin_time_tuple.tm_year
                i_time = int(origin_time_tuple.tm_year)
                #i_time = int(time.mktime(origin_time_tuple))
                if i_time <= 1970:
                    i_time = 0
                else:
                    i_time = long(time.mktime(origin_time_tuple))
                item['time'] = i_time * 1000
                item['suggest'] = '' if record['title'] is None else record['title']
                author = '' if record['author'] is None else record['author']
                item['author'] = author
                publisher = '' if record['publish'] is None else record['publish']
                item['publish'] = publisher
                industry = '' if record['industryname'] is None else record['industryname']
                item['industry'] = industry
                tags = '' if 'tag' not in record or record['tag'] is None else record['tag']
                item['tags'] = tags
                honor = '' if 'honor' not in record or record['honor'] is None else record['honor']
                item['honor'] = honor
            else:

                self.__id_list.append(item['image_id']+'\n')
                if 'source_type' in item:
                    item['title'] = item['source_type']
                else:
                    item['title'] = ''
                #item['title'] = ''
                item['type'] = ''
                item['summary'] = ''
                item['company'] = ''
                item['stockcode'] = ''
                item['time'] = 0
                item['year'] = 0
                item['publish'] = ''
                item['tags'] = ''
                #logging.warn('Failed to get report by src id:' + str(chart_item['fileId']))
                continue


            # doc feature
            # doc feature
            doc_feature = self._chart_duplicate.getDocumentFeature(item)
            item['doc_feature'] = doc_feature

            if len(self.__tempfile) > 0:
                arr = self.__tempfile.get(item['image_id'])
                if arr is not None:
                    item['image_title'] = arr[1]
                    item['doc_score'] = arr[2]

            data.append(item)

        mysql.close()
        logging.info('End __buildUpdateItems')
        return data, id_list


    def convertRecordsToArray(self, chart_items):
        data = []
        for chart_item in chart_items:
            data.append(chart_item)

        return data

    def getReportItemBySrcId(self, src_id):
        mysql = Mysqldb.getMysqlInstance()
        find_sql = "select * from hibor where id = %s limit 1"
        args = (str(src_id),)
        cursor = mysql.cursor()
        row = None
        try:
            cursor.execute(find_sql, args)
            row = cursor.fetchone()
            if row is not None:
                row = tool.convertRowToKeyValue(cursor, row)
        except Error as error:
            logging.error('Failed to find record, error:{}'.format(error))
            logging.error('sql:' + find_sql + ', src id:' + str(src_id))
        finally:
            cursor.close()

        mysql.close()
        return row


    def pushIndex(self, data, thread_id):
        if len(data) == 0:
            return 200

        #solr_api_list = config.getChartSolrAPI()['SOLR_CHAT_UPDATE_SSD_123']
        solr_api_list = config.getChartSolrAPI()['SOLR_CHAT_UPDATE_SSD_456']
        #solr_api_list = config.getChartSolrAPI()['SOLR_CHAT_UPDATE_PART_SSD_1']
        #solr_api_list = config.getChartSolrAPI()['SOLR_CHAT_UPDATE_PART_SSD_4']
        #solr_api_list = config.getChartSolrAPI()['SOLR_CHAT_UPDATE_9']


        solr_api = solr_api_list[thread_id % len(solr_api_list)]
        logging.info('Start to push data, api:' + solr_api)
        code = SolrServer.sendRequest(solr_api, data)

        logging.info("Finished to push data, api:" + solr_api + "; code:" + str(code))

        # push some data to test server
        #solr_api_test = 'http://10.168.20.246:8080/solrweb/chartIndexByUpdate?origin_from=raa'
        #solr_api_test = 'http://10.12.0.84:8080/solrweb/chartIndexByUpdate?origin_from=raa&local=true'
        #code = SolrServer.sendRequest(solr_api_test, data)
        #logging.info("Finished to push data, api:" + solr_api_test + "; code:" + str(code))

        return code
