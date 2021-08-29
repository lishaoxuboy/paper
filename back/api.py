import tornado.web
import os

from common.log import Lzlog
from common.base_http import BaseHttp
from common.public_mthod import param_diff, catch_error, timestamp
from control import User_Control, Check_User, Verification, Paper_Control, AlipayControl, WeChatPay, Order
import base64


class User(BaseHttp):

    def post(self):
        """
        新增用户
        :param args:
        :param kwargs:
        :return:
        """
        Lzlog.info(" %s 添加用户 %s" % (self.request.remote_ip, self.data))
        diff = param_diff(param=["name", "account", "password", "code", "email_addr"], _in=self.data)
        if diff:
            self.write(self.get_res(-1, "缺少参数 %s" % diff))
        elif Check_User.is_exisit(self.data):
            self.write(self.get_res(-2, "用户名已存在" % diff))
        else:
            # 获取邮箱验证码
            send_code = Verification.get_send_record(self.data["name"] + self.data["account"] + self.data["email_addr"])
            if send_code and send_code == self.data["code"]:
                self.write(User_Control.add_user(self.data))
            else:
                self.write(self.get_res(-3, "验证码不正确，请检查账号、邮箱是否正确，然后再试！"))

    def put(self):
        """
        用户修改密码
        :return:
        """
        Lzlog.info(" %s 修改或者找回密码 %s" % (self.request.remote_ip, self.data))
        diff = param_diff(param=["old_pwd", "new_pwd", "type", "code", "email_addr"], _in=self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        send_record = Verification.get_send_record(base64.b64encode(self.data["email_addr"].encode()).decode())
        if send_record and send_record == self.data["code"]:
            # 用户在个人主页修改密码（在记得密码的情况下,需要输入老密码）
            if self.data["type"] == 1:
                return self.write(User_Control.update_pwd(self.data))
            else:
                # 用户在登录界面修改密码（在不记得密码的情况下，邮箱验证后，不需要输入老密码）
                return self.write(User_Control.reset_pwd(self.data))
        elif send_record is False:
            return self.write(self.get_res(1, "验证码已失效，请稍后重新发送！"))
        else:
            return self.write(self.get_res(1, "验证码有误，请稍后重新发送！"))



class Login(BaseHttp):
    """处理登录 登出"""

    def post(self):
        """
        登录
        :return:
        """
        data = self.get_data()
        diff = param_diff(param=["account", "password", "type"], _in=data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))

        res = Check_User.account_pwd_exisit(data)
        if not res:
            return self.write(self.get_res(-1, "用户名或密码不正确"))
        else:
            session = self.gen_session()
            self.push_session(session, res)  # 保存当前用户信息
            self.write(self.get_res(data=dict(id=res.id,
                                              roleType=res.role,
                                              name=res.name,
                                              account=res.account,
                                              email_addr=res.email_addr,
                                              session=session)))

    def delete(self):
        """
        登出
        :return:
        """
        try:
            diff = param_diff(param=["session"], _in=self.data)
            if diff:
                return self.write(self.get_res(-1, "缺少参数 %s" % diff))
            if self.unregister(self.data['session']):
                return self.write(self.get_res())
            else:
                return self.write(self.get_res(0, "用户未登录"))
        except Exception as e:
            Lzlog.info("用户退出异常 %s" % e)
            return self.write(self.get_res(-1, "内部异常"))

    def get(self):
        """"""
        self.write(self.get_res(-1000, msg="没有登陆"))


class Email(BaseHttp):
    """
    向指定邮箱发送指定内容
    """
    def post(self):
        data = self.get_data()
        diff = param_diff(param=["name", "account", "email_addr", "type"], _in=data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        # 发送注册验证码
        if data["type"] == 1:
            uuid = data["name"] + data["account"] + data["email_addr"]
            operation = "注册账号"
            res = User_Control.check_user_exists(self.data["name"], self.data["account"], self.data["email_addr"])
            if res["code"] != 0:
                return self.write(res)
        else:
            res = User_Control.check_user_exists(email_addr=data["email_addr"])
            # code == -3 代表邮箱已存在，可以找回密码
            if res["code"] != -3:
                return self.write(self.get_res(-3, msg="没有用户绑定该邮箱"))
            # 发送找回密码验证码
            operation = "密码找回"
            uuid = base64.b64encode(data["email_addr"].encode("utf-8")).decode()


        Verification.send_to(data["email_addr"], Verification.gen_code(), uuid, operation)
        return self.write(self.get_res(0, msg="验证码发送成功（受网络影响，接收可能存在延迟，请不要重复发送，以免验证失败）！"))


class Paper(BaseHttp):
    """
    论文的增删改查
    """

    def post(self):
        need_params = ["name", "key_word", "abstract", "pdf_path", "word_path", "author_list"]
        user = self.get_user_info()
        if not user:
            return self.set_status(403, "用户未登录")
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        res = Paper_Control.add(self.data)
        return self.write(res)

    @tornado.web.authenticated
    def delete(self):
        need_params = ["id"]
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        return self.write(Paper_Control.delete(self.data))

    @tornado.web.authenticated
    def put(self):
        need_params = ["id", "name", "key_word", "abstract", "pdf_path", "word_path", "author_list", "comments", "status", "money"]
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))

        res = Paper_Control.update_paper(self.data)
        return self.write(res)

    @tornado.web.authenticated
    def get(self):
        user_info = self.get_user_info()
        data = self.get_data()
        if not user_info:
            self.set_status(403, "用户未登录")
            return self.write("")
        user_type = int(user_info.role)
        user_id = int(user_info.id)
        page_number = int(data.get("pagenum", 1))
        page_size = int(data.get("pagesize", 10))
        self.write(Paper_Control.get_paper(user_id, user_type, page_number, page_size))


class Upload(BaseHttp):

    # @tornado.web.authenticated
    @catch_error
    def post(self):
        if self.request.files:
            file = self.request.files['file'][0]
            body = file["body"]
            file_type = file["filename"].split(".", maxsplit=1)[1]
            new_file_name = self.gen_session() + ".%s" % file_type
            save_path = os.path.join(os.path.dirname(__file__), "static", "uploads")
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            abs_path = os.path.join(save_path, new_file_name)
            with open(abs_path, "wb") as fp:
                fp.write(body)
            relative_path = os.path.join("static", "uploads", new_file_name)
            self.write(self.get_res(data=dict(save_path=relative_path, old_name=file["filename"])))
        else:
            self.write(self.get_res(-1, "文件不能为空"))


class AlipayHandler(BaseHttp):

    def post(self):
        """支付成功后收到支付宝通知

        """
        # 移除验签不需要的字段
        self.data.pop("sign_type", None)
        sign = self.data.pop('sign', None)
        self.data.pop('user_info', None)
        AlipayControl.verify(self.data, sign)
        self.write("success")


    def put(self):
        """调起支付界面"""
        need_params = ["money", "number", "title"]
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        try:
            try:
                money = float(self.data["money"])
            except:
                return self.write(self.get_res(-1, "支付金额有误!"))
            if money > 10**8 or money < 0:
                return self.write(self.get_res(-1, "付款金额在0.1~100000000"))
            number = self.data["number"] + "-" + str(timestamp())
            base64_qr_code = AlipayControl.go_pay(self.data["title"], number, money)
            return self.write(self.get_res(data=base64_qr_code))
        except Exception as e:
            return self.write(self.get_res(-1, "系统异常" + str(e)))


class WeChatPayHandler(BaseHttp):
    def post(self):
        """微信支付成功后"""
        """
        11111111621428247
        16210862781621428000
        16210862781621428772
        16210862781621429480
        16210862781621433546
        """
        body  = self.request.body
        WeChatPay.verify(body)
        return self.write("success")


    def put(self):
        """调起支付界面"""
        need_params = ["money", "number", "title"]
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        try:
            # 单位为分
            try:
                money = float(self.data["money"])
            except:
                return self.write(self.get_res(-1, "支付金额有误!"))
            if money > 10**8 or money < 0:
                return self.write(self.get_res(-1, "付款金额在0.1~100000000"))
            money = int(money * 100)
            base64_qr_code = WeChatPay.go_pay(
                self.data["title"],
                self.data["number"] + "-" + str(timestamp()),
                money)
            return self.write(self.get_res(data=base64_qr_code))
        except Exception as e:
            return self.write(self.get_res(-1, "系统异常!" + str(e)))


class OrderPayRes(BaseHttp):
    def get(self):
        need_params = ["number"]
        diff = param_diff(need_params, self.data)
        if diff:
            return self.write(self.get_res(-1, "缺少参数 %s" % diff))
        return self.write(self.get_res(data=Order.is_pay_success(self.data["number"])))
