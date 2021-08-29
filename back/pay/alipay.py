# _*_ coding=utf-8 _*_
from datetime import datetime
from urllib.parse import quote_plus
from common.public_mthod import ordered_dict, join_tuple_param, rsa_sign, read_secret, generate_qr_code, rsa_verify_sign, join_tuple_param_alipay
from settings.config import Conf_Impl

import json
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import encodebytes, decodebytes
import requests


class AliPay(object):
    """
    支付宝支付接口(PC端支付接口)
    """

    def __init__(self, appid, app_private_key_path, alipay_public_key_path, app_notify_url, return_url):
        self.appid = appid
        self.app_key_path = app_private_key_path
        self.alipy_key_path = alipay_public_key_path
        self.app_notify_url = app_notify_url
        self.return_url = return_url


    def create_pay(self, subject, out_trade_no, total_amount, notify_url, redirect_url, **kwargs):
        """
        创建订单
        :param subject: 订单主题
        :param out_trade_no: 订单号
        :param total_amount: 订单金额，单位：元，精确位数：2，示例：6.66
        :param notify_url: 支付成功通知地址
        :param redirect_url: 支付成功后重定向定制
        :param kwargs: 扩展信息
        :return:
        """
        body = dict(
            app_id=self.appid,  # 应用id
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notify_url=notify_url,
            return_url=redirect_url,
            charset="utf-8",
            sign_type="RSA2",
            version="1.0",
            # method="alipay.trade.page.pay",
            method="alipay.trade.precreate",
            biz_content=dict(   # 订单基本内容
                out_trade_no=out_trade_no,
                qr_code_timeout_express="90m",
                subject=subject,
                total_amount=total_amount
                # product_code="FAST_INSTANT_TRADE_PAY",
            )
        )
        # 支持扩展字段
        body["biz_content"].update(kwargs)
        # 将传递的参数进行排队，接口对接要求
        unsigned_items = ordered_dict(body)
        # 在使用&符号将参赛连接起来
        unsigned_string = join_tuple_param(unsigned_items)
        # 签名
        sign = rsa_sign(unsigned_string.encode("utf-8"), self.app_key_path, key_is_file=True)
        # 在使用&符号将参赛连接起来
        query_parma = join_tuple_param(unsigned_items, quote_plus=True)
        # 拼接查询参数
        signed_string = query_parma + "&sign=" + quote_plus(sign)
        response = requests.get(alipay_conf.pay_url + signed_string)
        if response.ok:
            res_data = response.json()
            main_data = res_data["alipay_trade_precreate_response"]
            if main_data["code"] == "10000":
                response_sign = res_data.pop("sign")
                # 将传递的参数进行排队，接口对接要求
                # 在使用&符号将参赛连接起来
                response_unsigned_items = ordered_dict(main_data)
                response_unsigned_string = join_tuple_param_alipay(response_unsigned_items)
                res = rsa_verify_sign(response_unsigned_string, response_sign, self.alipy_key_path, key_is_file=True)
                if res_data["alipay_trade_precreate_response"]["code"] == "10000" and res:
                    return generate_qr_code(res_data["alipay_trade_precreate_response"]["qr_code"])
        return None

    def sign_data(self, data: dict):
        data.pop("sign", None)
        # 将传递的参数进行排队，接口对接要求
        unsigned_items = ordered_dict(data)
        # 在使用&符号将参赛连接起来
        unsigned_string = join_tuple_param(unsigned_items)
        # unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 将数据签名，返回是一个经过base64编码的字符串
        sign = self.sign(unsigned_string.encode("utf-8"))
        # 然后拼接url请求参数，这里注意，应为跳转到页面是使用get请求，这时候如果请求的参数值为字典，就需要进行编码
        # 就是name或者value中出现了=、&就会出问题，所以这里使用quote_plus函数就是就这些字符进行编码
        """
        示例代码
        a = {
            "a": 1,
            "b": 2,
            "c": {
                "d":3,
                "e":4
            }
        }
        for k, v in a.items():
            if isinstance(v, dict):
                a[k] = json.dumps(v, separators=(",", ""))
        print("&".join("{0}={1}".format(k, quote(str(v).encode())) for k, v in a.items()))
        >>:a=1&b=2&c=%7B%22d%223%2C%22e%224%7D
        """
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        print(signed_string)
        return signed_string


    @staticmethod
    def ordered_data(data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名

        key = read_secret(self.app_key_path)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


# 应用的私钥
# private_key = """-----BEGIN RSA PRIVATE KEY-----
# MIIEowIBAAKCAQEAl0pU2tm6ieeK4N2AJmIhHg20FbX0ze7W3DBa+o+MpwdimqFdscqAOA+jyU9esdn4QQMB3+yVtzKsjO4UbpnNBGXE2/oHGzpAxCIgYP0QxCNF7ZYLbgs8kSrFzWRsp8JtyIQnDtuqCjYkLQGtewKsOoJIGg1qctjbGfPobNpwECCxLQ/Nns3nBuVg2NR6kXmI/qKV6qr3TMscA7bUPVk2HhRsAX9STOMHEKfEyK/lBxD52TfNnVL+U4YYFFyyiusrJpE5gAOPgc+XW4MpOBCIduic/+9prD/i4PTdv7N2XsQjgOkfdpprVJySc+HUcFMXpE+E0d71FZj+EIHnPZYBJQIDAQABAoIBAA7TyyMzyZNwbO0C6GdaoLJIV4j1L0vrh4VG+/Ook/lewOw0unENTqmv5rZ5H+fAXBNLDyj6D+ZHgh/ByaDZU/2FV9jTVVT2zZgrXA8FXlpKtrTFStN7KHF1xrMNj5SVepr3ULilELI1gjAjBPSUW3rUf+qFvBQLatXNUM8yTV9XHT5X8NyAx/RIyINTjSVIIjaq81uxwq5DpXPwOkPBskgA/J4ozTfdxlm+OKZ5/o4Pd/3ulmrkdwnJmmmHNIYWJgTwlFxUpEeF1DO5Erk+t+bVAM6j28H3F045FcB1HqvhKrjfjVSEIXy4CVyBt8TLQmGEkW91MtYk0RP1/b8l8yECgYEA+TRVy4UAmeAnJFGN9h0oI4QN8kjj0KiTx7Gl7xRQvoc9t7XhKevcH9Dvs3XCRj2fvMA9d/xh1BoaZ8xLc4qwqEWYXgWxswo7kzEFtFmgJKQ88dPZPZYO3+Cd9vZUxwil1hZkJwQD/B04z4/zVagHqYJg06LW06XjGqcMfIv56AkCgYEAm2p4b4efIQb83AfkAzSdn2YMP5DVhjeNtdOnL9o84JV5DlNz7zKiS9OlAB4sCOInECm8BkE19eHeoKcFfHz+SJCY1JYPWxXii4mTzGG1p7eIK69Ev7khxpDiZrSHpwvU8SVlmFmophrpPQeZq0gxosrOupbA70hs8Q1EZ5RTvz0CgYBMAR45mDL6u1a0yPrXGUVor5nhT0HMHd4UhaXqKPQHaA/2u84Ujw7v1TWGMmAyNBFH7AnTUnIz0lJDXheVAbOnXrJ92pa72F8bIVRwEPW6tyyvRMF4+w9GUKdc7vwkSArsJKAfFiZw+iidhXXdpgXQOSd25K9IlcuSEWjJg5eQoQKBgA50LXU56Lu6maOg/DysFQixBeyXfLQ50G0bnQ3fPxAn9pU1f6+8RsnEijDjnXbKCZYAO6NdRzZx5jGMtv7n5QI8qGoE9rKi62nMxrkYUTui3wApEby+6/w6l0O0AHWxrQEsWDF+DSg9knmBjnIWib85G1bRFGpsku0sLbNwYQWFAoGBAO6evUG81bFcf0smIxbqCBBeYbn3E9mWZnQ0UnG0hW3JyLtT/rOkYEDFa4Zdfns5xD7Blx7Eh2oQsafThbReVsPIrE/qEGjQE2g+ZUGLGxv2sdJKpTHbuqsJSMIFmNOKdhzV+BQG+I8YcOsJyqmb+nU9lwdeyWTq3kh1lXb73aBS
# -----END RSA PRIVATE KEY-----"""
# # alipay的公钥
# public_key = """-----BEGIN RSA PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnNf1Fo39VdghVcWv8RCb6MYdZyw8WP9vYGkTIFVVyFGMEJX2WM74+K6JOneCrB8k0DZBmDn9uphuWrmchUxeDRPJ3I0mV3k+ygC4lr/lZfc8thMiK8e/keH5fCLiNYEkNAYrRSpSxkeffWE3Yng0/IsQ9Z8kiut55wngDrv4hVgPUIiNNFP3JlHGTh94S9B9WnJzaKzvND2xsNAQW2MG+ndcULBsTssfMGiJSke58zJqKXpeqRDkuEQZIl0huSrcezM/MZgLU4OkDRvKzjjgc4TmT3ZzvAQqOdddbz8G0/ee381Ll4qBvFl8EzN4CeiueNophLLwG1i31czetuKFdQIDAQAB
# -----END RSA PUBLIC  KEY-----"""
alipay_conf = Conf_Impl.get_alipy_config()
alipay_impl = AliPay(
    appid=alipay_conf.app_id,  # 支付宝沙箱里面的APPID
    app_private_key_path=alipay_conf.app_key_path,  # 支付宝公钥
    alipay_public_key_path=alipay_conf.ali_key_path,  # 应用私钥
    app_notify_url=alipay_conf.notify_url,  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问
    return_url=alipay_conf.redirect_url,  # 如果支付成功，重定向回到你的网站的地址。
)