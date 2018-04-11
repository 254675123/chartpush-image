# -*- coding: utf-8 -*-
# coding=utf-8


# convert index value into key-value
import mysql
from mysql import connector


def convertRowToKeyValue(cursor, row):
    columns = [desc[0] for desc in cursor.description]

    result = {}
    for k, v in zip(columns, row):
        result[k] = v

    return result


class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)
