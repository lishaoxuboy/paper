"""
启动文件
"""

import tornado.ioloop
import tornado.web
from api import User, Login, Email, Paper, Upload, AlipayHandler, WeChatPayHandler, OrderPayRes
from common.log import Lzlog
from common.database import Database_Impl
import os


class StaticHandler(tornado.web.StaticFileHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE')

    def options(self, *args, **kwargs):
        pass


class Index(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.redirect("index.html")


settings = {
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    "login_url": "/login",
    "static_path": "static"
}

if __name__ == '__main__':
    current_path = os.path.dirname(__file__)  # 上一层目录
    app = tornado.web.Application([
        (r'/', Index),
        (r'/user', User),
        (r'/login', Login),
        (r'/verification', Email),
        (r'/paper', Paper),
        (r'/upload', Upload),
        (r'/alipay', AlipayHandler),
        (r'/wechatpay', WeChatPayHandler),
        (r'/order_status', OrderPayRes),
        (r"/(.*)", StaticHandler, {"path": os.path.join(current_path, "static")})
    ], **settings)
    port = 1122
    app.listen(port)
    Lzlog.info("service start at http://0.0.0.0:%d" % port)

    drop_all = False
    # drop_list = [Paper_Module.__table__]
    drop_list = []
    if not drop_all and drop_list:
        print("重建部分表 %s" % [i.name for i in drop_list])
        Database_Impl.drop_all(drop_list)
        Database_Impl.create_all(drop_list)
    elif drop_all:
        print("重建所有表")
        Database_Impl.drop_all([])
        Database_Impl.create_all([])
    tornado.ioloop.IOLoop.current().start()
