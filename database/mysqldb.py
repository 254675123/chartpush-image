# -*- coding: utf-8 -*-
# coding=utf-8

import mysql.connector
import logging
from config import database
from database.tool import NumpyMySQLConverter


class Mysqldb:
    def __init__(self):
        pass

    @staticmethod
    def getMysqlInstance():
        db = Mysqldb.__getMysqlConnection()
        db .set_converter_class(NumpyMySQLConverter)
        return db

    # connect to mysql
    @staticmethod
    def __getMysqlConnection():
        """ Connect to MySQL database """
        mysql_config = database.getMysqlConfig()

        conn = mysql.connector.connect(host=mysql_config['MYSQL_HOST'],
                                       database=mysql_config[
                                           'MYSQL_DATABASE'],
                                       port=mysql_config['MYSQL_PORT'],
                                       user=mysql_config['MYSQL_USER'],
                                       password=mysql_config[
                                           'MYSQL_PASSWORD'])
        if conn.is_connected():
            return conn
        else:
            logging.error('Failed to connect to MySQL database')
            return None
