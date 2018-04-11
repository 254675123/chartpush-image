# -*- coding: utf-8 -*-
# coding=utf-8
import json
import logging
import requests
from requests import ConnectionError


class SolrServer:
    def __init__(self):
        pass

    @staticmethod
    def sendRequest(url, data):
        headers = {'Content-type': 'application/json'}
        try:
            r = requests.post(url, json=data, headers=headers)
        except ConnectionError as error:
            logging.error('Failed to send requeust, error:{}'.format(error))
            return -1
        except TypeError as error:
            logging.error(data)

        if r.status_code == 200:
            return json.JSONDecoder().decode(r._content)['code']
        return r.status_code
