# -*- coding: utf-8 -*-
# coding=utf-8

import argparse
import logging

from config import config
from solr.chart_pusher_image import ChartPusher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research Reporter Tool.")
    parser.add_argument('-t', '--target', nargs='?', type=str, default=0)
    args = parser.parse_args()

    # init config
    config.init()

    logging.info('Start to run')

    # 推送识别出来的图
    ChartPusher.start(args.target)

