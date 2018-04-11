# -*- coding: utf-8 -*-
# coding=utf-8
import hashlib
import sys

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

class ChartDuplicate:
    """
    image duplicate remove
    """

    def __init__(self):
        self.__sleep_time_per_request = 0.01
        self.__sleep_time_per_request_none = 180.00


    # 排重规则说明
    # 1. image_title, legends 任意一个为空, 则返回空
    # 2. stock code 移除前后空格,如果长度大于3则视为有效,否则该值为空
    # 3. source 需要除掉无关字,例如:年,月,日,来源于,获取于
    def getDocumentFeature(self,item):

        # image url 为空 return 空
        image_url = item['image_url']
        if image_url == '':
            return ''

        # image title
        # if image title is empty ,return
        image_title = item['image_title']
        image_title = image_title.strip()
        length = len(image_title)
        if image_title == '' or length < 2:
            return ''
        # 去掉冒号及前面的内容
        index = image_title.find(':')
        if (index < 0):
            index = image_title.find('：')

        if index > 0 and index + 1 < length:
            image_title = image_title[index + 1:]


        # image legends
        image_legends = item['image_legends']


        # company stock code
        stock_code = item['stockcode']


        # doc_feature = ''
        doc_feature = image_title.strip() + '--' + image_legends + '--' + stock_code

        md5 = self.getMd5(doc_feature)

        return md5


    def getMd5(self,text):

        md5 = hashlib.md5(text.encode('utf-8')).hexdigest()

        return md5

#ste = '图38：着急防风'
#index = ste.find('：')
#sub_str = ste[index:]
#print index
