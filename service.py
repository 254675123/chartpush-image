# -*- coding: utf-8 -*-
# coding=utf-8

import time
import tornado.web
from tornado.options import options
from solr.chart_pusher_image import ChartPusher

tornado.options.define('port', default=8888, help='run on this port', type=int)
#tornado.options.define("log_file_prefix", default='tornado_8888.log')
tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        start = time.time()
        image_ids = self.get_argument('ids')

        # 打印信息
        print('==========>')
        print("[INFO]开始处理本次请求:" + str(image_ids))

        # 处理句子
        result_list = ChartPusher.start(image_ids)
        res = ','.join(result_list)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write(res)
        print("[INFO]本次耗时" + str((time.time() - start)*1000) + "ms")

        return

    def post(self):
        self.get()


if __name__ == "__main__":

    settings = {
        'template_path': 'views',  # html文件
        'static_path': 'statics',  # 静态文件（css,js,img）
        'static_url_prefix': '/statics/',  # 静态文件前缀
        'cookie_secret': 'adm',  # cookie自定义字符串加盐
    }

    application = tornado.web.Application([(r"/", MainHandler), ], **settings)
    application.listen(options.port)
    print("SERVICE 已经开启！")
    tornado.ioloop.IOLoop.instance().start()
