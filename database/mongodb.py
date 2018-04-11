# -*- coding: utf-8 -*-
# coding=utf-8

import pymongo
import logging
from config import database


class Mongodb:
    def __init__(self):
        pass

    __mongodb_instance = None

    @staticmethod
    def getMongodbCollection(collection, ):
        if Mongodb.__mongodb_instance is None:
            Mongodb.__initMongodbInstance()

        if Mongodb.__mongodb_instance is None:
            return None

        return Mongodb.__mongodb_instance[collection]

    @staticmethod
    def __initMongodbInstance():
        if Mongodb.__mongodb_instance is None:
            Mongodb.__mongodb_instance = Mongodb.__getMongodbConnection()

        if Mongodb.__mongodb_instance is None:
            logging.error('Failed to connect to MySQL database')

        return Mongodb.__mongodb_instance

    # connect to mongodb
    @staticmethod
    def __getMongodbConnection():
        """
        Connect to Mongodb database
        """
        mongodb_config = database.getMongodbConfig()
        client = pymongo.MongoClient(mongodb_config['MONGO_URI'],appname='chart_push')

        return client[mongodb_config['MONGO_DATABASE']]
