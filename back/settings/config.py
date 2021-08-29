# --coding:utf-8--
"""
加载程序运行所需的所有配置
"""
import configparser

from common.public_mthod import Dict


class Config:
    _conf_impl = None

    def __init__(self):
        """
        辅助类完成实例的一些函数可以定义为类方法
        实例对象调用的方法为实例方法
        在类中完成特定功能的与类逻辑不相干的可定义为静态方法
        """
        self._load_db_conf()
        self._load_alipy_config()
        self._load_wechatpay_config()
        self._load_email_config()

    @classmethod
    def generate_conf_impl(cls) -> configparser.ConfigParser:
        """
        返回一个可以读取配置文件的实例
        :return: configparser.ConfigParser()
        """
        if cls._conf_impl is None:
            conf_impl = configparser.ConfigParser()
            conf_impl.read("static/config.ini", "utf-8")
            cls._conf_impl = conf_impl
            return conf_impl
        else:
            return cls._conf_impl

    @classmethod
    def get_option_value(cls, section, option, default=None):
        return cls.generate_conf_impl().get(section, option, fallback=default)

    @classmethod
    def get_option_value_int(cls, section, option, default=None) -> int():
        return cls.generate_conf_impl().getint(section, option, fallback=default)

    def _load_db_conf(self):
        self.db_conf = Dict()
        self.db_conf.host = self.get_option_value("db", "host")
        self.db_conf.port = self.get_option_value_int("db", "port")
        self.db_conf.type = self.get_option_value("db", "type")
        self.db_conf.user = self.get_option_value("db", "user")
        self.db_conf.pad = self.get_option_value("db", "password")
        self.db_conf.db_name = self.get_option_value("db", "database")

    def get_db_conf(self):
        return self.db_conf

    def _load_alipy_config(self):
        self.alipay_conf = Dict()
        self.alipay_conf.ali_key_path = self.get_option_value("alipay", "ali_public_secret_key_path")
        self.alipay_conf.app_key_path = self.get_option_value("alipay", "app_private_secret_key_path")
        self.alipay_conf.app_id = self.get_option_value("alipay", "app_id")
        self.alipay_conf.notify_url = self.get_option_value("alipay", "notify_url")
        self.alipay_conf.redirect_url = self.get_option_value("alipay", "redirect_url")
        self.alipay_conf.pay_url = self.get_option_value("alipay", "pay_url")

    def get_alipy_config(self):
        return self.alipay_conf

    def _load_wechatpay_config(self):
        self.wechatpay_conf = Dict()
        self.wechatpay_conf.key_path = self.get_option_value("wechatpay", "wechat_secret_key_path")
        self.wechatpay_conf.app_id = self.get_option_value("wechatpay", "app_id")
        self.wechatpay_conf.mch_id = self.get_option_value("wechatpay", "mch_id")
        self.wechatpay_conf.notify_url = self.get_option_value("wechatpay", "notify_url")

    def get_wechatpay_config(self):
        return self.wechatpay_conf

    def _load_email_config(self):
        self.email_conf = Dict()
        self.email_conf["valid_minute"] = self.get_option_value("email", "valid_minute", 3)

    def get_email_config(self):
        return self.email_conf
    # def _load_paper_status_map(self):
    #     self.paper_status_map = Dict()
    #     self.paper_status_map.key_path = eval(self.get_option_value("paper", "status_map"))

    # def get_paper_status_map(self, reverse=False):
    #     if reverse:
    #         return dict([(v, k) for k,v in self.paper_status_map.items()])
    #     else:
    #         return self.paper_status_map


Conf_Impl = Config()
