import requests
from settings.config import Conf_Impl
from copy import deepcopy
from common.log import Lzlog
from common.public_mthod import timestamp, sign_md5, xml_to_dict, dicttoxml, \
    generate_qr_code, ordered_dict, join_tuple_param, read_secret


class WechatPay:
    def __init__(self):
        self.conf = Conf_Impl.get_wechatpay_config()
        self.app_id = self.conf["app_id"]
        self.mchid = self.conf["mch_id"]
        self.notify_url = self.conf["notify_url"]
        with open(self.conf["key_path"], "r") as fp:
            self.key_secert = fp.read()

    def create_pay(self, title, number, money):
        try:
            body = dict()
            body["appid"] = self.app_id
            body["mch_id"] = self.mchid
            body["nonce_str"] = str(timestamp())
            body["body"] = title
            body["out_trade_no"] = number
            body["total_fee"] = money
            body["spbill_create_ip"] = "127.0.0.1"
            body["notify_url"] = self.notify_url
            body["trade_type"] = "NATIVE"

            a = sorted([(k, v) for k, v in body.items()])
            param = "&".join(["{0}={1}".format(k, v) for k, v in a]) + "&key=" + self.key_secert
            sign = sign_md5(param.encode("utf-8"))
            body["sign"] = sign
            title = dict(xml=body)
            request_data = dicttoxml(title)
            response = requests.post(url="https://api.mch.weixin.qq.com/pay/unifiedorder",
                                     data=request_data.encode("utf-8"))
            if response.status_code == 200:
                res = xml_to_dict(response.text)
                sign = res["xml"].pop("sign", None)
                unsigned_item = ordered_dict(deepcopy(res["xml"]))
                key_path = Conf_Impl.get_wechatpay_config()["key_path"]
                key = read_secret(key_path, import_key=False)
                unsinged_str = join_tuple_param(unsigned_item) + "&key=" + key
                if sign == sign_md5(unsinged_str.encode()).upper():
                    if res["xml"]["return_code"] == "SUCCESS" and res["xml"]["result_code"] == "SUCCESS":
                        return generate_qr_code(res["xml"]["code_url"])
                else:
                    Lzlog.error("订单创建信息有误：签名不正确")
                    return False
        except Exception as e:
            print("支付错误", e)
        return False


wechat_pay = WechatPay()
