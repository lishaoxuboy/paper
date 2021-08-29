import datetime
import random
from copy import deepcopy
from sqlalchemy import func
from modules import User_Module, Paper_Module, Author_Module
from common.database import Database_Impl
from common.public_mthod import catch_error, get_res, now_datetime, file_base_name, ordered_dict, \
    join_tuple_param, rsa_verify_sign, xml_to_dict, sign_md5, long_timestamp
from common.my_email import send_email
from pay.alipay import alipay_impl
from pay.wechat import wechat_pay
from settings.config import Conf_Impl
from common.log import Lzlog


class User_Control:
    """
    实现用户的增删改查
    """

    @staticmethod
    @catch_error
    def add_user(data):
        with Database_Impl.get_db_session() as DB:
            md5_pwd = sign_md5(data.password.encode("utf-8"))
            user = User_Module(name=data.name, account=data.account, password=md5_pwd, email_addr=data.email_addr)
            DB.add(user)
            DB.flush()
            insert_id = user.id
            DB.commit()
            return get_res(data=insert_id)

    @staticmethod
    @catch_error
    def update_pwd(data):
        with Database_Impl.get_db_session() as DB:
            md5_pwd = sign_md5(data.old_pwd.encode("utf-8"))
            user = DB.query(User_Module).filter(User_Module.id == data.user_info.id,
                                               User_Module.password == md5_pwd).first()
            if not user:
                return get_res(-1, "旧密码不正确")
            user.password = sign_md5(data.new_pwd.encode("utf-8"))
            DB.commit()
            return get_res(0)

    @staticmethod
    @catch_error
    def reset_pwd(data):
        with Database_Impl.get_db_session() as DB:
            user = DB.query(User_Module).filter(User_Module.email_addr == data.email_addr).first()
            if user:
                user.password = sign_md5(data["new_pwd"].encode("utf-8"))
                DB.commit()
                return get_res(0)
            else:
                return get_res(1, "未找到用户")

    @classmethod
    def check_user_exists(cls, name=None, account=None, email_addr=None):
        if not name and not account and not email_addr:
            return get_res(0)
        with Database_Impl.get_db_session() as DB:
            name_exists = False
            account_exists = False
            email_exists = False
            if name and DB.query(User_Module).filter(User_Module.name == name).first():
                account_exists = True
            if account and DB.query(User_Module).filter(User_Module.account == account).first():
                account_exists = True
            if email_addr and DB.query(User_Module).filter(User_Module.email_addr == email_addr).first():
                email_exists = True

            if not name_exists and not account_exists and not email_exists:
                return get_res(0)
            elif name_exists:
                return get_res(-2, "该用户名已被注册")
            elif account_exists:
                return get_res(-1, "该账号已被注册")
            else:
                return get_res(-3, "该用邮箱已被注册")


class Check_User:
    """
    用户相关信息检查
    """

    @staticmethod
    def account_pwd_exisit(data) -> [User_Module]:
        with Database_Impl.get_db_session() as DB:
            pwd = sign_md5(data.password.encode("utf-8"))
            if data["type"] == 1:
                res = DB.query(User_Module).filter(User_Module.account == data.account,
                                                   User_Module.password == pwd).all()
            else:
                res = DB.query(User_Module).filter(User_Module.email_addr == data.account,
                                                   User_Module.password == pwd).all()
            return res[0] if res else False

    @staticmethod
    def is_exisit(data) -> bool:
        with Database_Impl.get_db_session() as DB:
            res = DB.query(User_Module).filter(User_Module.account == data.account, User_Module.name == data.name).all()
            return res[0] if res else False


class Verification:
    send_record = dict()

    @classmethod
    def gen_code(cls):
        return str(random.randint(100000, 999999))

    @classmethod
    def send_to(cls, send_to, code, uuid, operation):
        valid_minute = int(Conf_Impl.get_email_config().get("valid_minute"))
        cls.send_record[uuid] = dict(
            addr=send_to,
            code=code,
            expiration_time=datetime.datetime.strftime(
                datetime.datetime.now() + datetime.timedelta(minutes=valid_minute), "%Y-%m-%d %H:%M:%S")
        )
        return send_email(send_to, code, valid_minute, operation)

    @classmethod
    def get_send_record(cls, uuid):
        record = cls.send_record.get(uuid, None)
        if record:
            if datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") <= record["expiration_time"]:
                return record["code"]
            else:
                # 代表过期
                return False
        else:
            # 代表没有获取到
            return None


class Paper_Control:
    """
    论文的CURD
    """
    @staticmethod
    @catch_error
    def add(data):
        with Database_Impl.get_db_session() as DB:
            paper = Paper_Module(name=data.name,
                                 number=long_timestamp(),
                                 key_word=data.key_word,
                                 abstract=data.abstract,
                                 pdf_path=data.pdf_path,
                                 word_path=data.word_path,
                                 user_id=data.user_info.id,
                                 create_date=now_datetime(),
                                 pdf_name=data.pdf_name,
                                 word_name=data.word_name,
                                 )
            # 先添加论文
            DB.add(paper)
            DB.flush()
            # 获取论文id
            paper_id = paper.id

            # 然后添加作者，并且与论文绑定
            manage_author_id = 0
            for i in data["author_list"]:
                new = Author_Module(name=i["author_name"], english_name=i["english_name"],
                                    org=i["org"], email=i["email"],
                                    addr=i["addr"], job_title=i["job_title"],
                                    phone=i["phone"], wechat=i["wechat"],
                                    paper_id=paper_id
                                    )
                DB.add(new)
                DB.flush()
                # 尝试获取这篇论文的管理作者
                if i.get("manage") == '1' and not manage_author_id:
                    manage_author_id = new.id

            # 在更新改论文的管理作者
            cur_paper = DB.query(Paper_Module).filter(Paper_Module.id == paper_id).first()
            cur_paper.manage_author_id = manage_author_id
            DB.commit()
            return get_res(data=paper_id)

    @staticmethod
    @catch_error
    def update_paper(data):
        with Database_Impl.get_db_session() as DB:
            paper_id = data.id
            # 获取论文，并更新论文信息
            paper = DB.query(Paper_Module).filter(Paper_Module.id == paper_id).first()
            # 如果是管理员，则修改批注信息
            if data.user_info and int(data.user_info.role) == 2:
                # 以下三个字段，只有管理员登录的时候才能修改
                paper.comments = data.comments
                paper.status = data.status
                paper.money = data.money
                DB.commit()
                return get_res()
            else:
                # 如果是普通用户，更新论文内容
                paper.name = data.name
                paper.key_word = data.key_word
                paper.abstract = data.abstract
                paper.pdf_path = data.pdf_path
                paper.word_path = data.word_path
                paper.pdf_name = data.pdf_name
                paper.word_name = data.word_name

                # 移除原有作者
                author_list = DB.query(Author_Module).filter(Author_Module.paper_id==paper_id).all()
                for i in author_list:
                    DB.delete(i)

                # 添加新的作者
                find_manage_author = False
                for i in data["author_list"]:
                    new = Author_Module(name=i["author_name"], english_name=i["english_name"],
                                        org=i["org"], email=i["email"],
                                        addr=i["addr"], job_title=i["job_title"],
                                        phone=i["phone"], wechat=i["wechat"],
                                        paper_id=paper_id
                                        )
                    DB.add(new)
                    DB.flush()
                    # 尝试获取这篇论文新的管理作者
                    if i.get("manage") and not find_manage_author:
                        find_manage_author = True
                        paper.manage_author_id = new.id
                        paper.manage_author_name = new.name
                DB.commit()
                return get_res()

    @classmethod
    @catch_error
    def delete(cls, data):
        paper_id = data.id
        with Database_Impl.get_db_session() as DB:
            # 找到论文并删除
            paper = DB.query(Paper_Module).filter(Paper_Module.id == int(paper_id)).first()
            if not paper:
                return get_res(-1, "没有找到该论文")
            DB.delete(paper)
            # 获取论文绑定的作者并删除
            author_list = DB.query(Author_Module).filter(Author_Module.paper_id == int(paper_id)).all()
            for i in author_list:
                DB.delete(i)
            DB.commit()
            return get_res(msg="删除成功")

    @classmethod
    @catch_error
    def get_paper(cls, user_id, user_type, page_number, page_size):
        # 论文列表
        paper_list = list()
        with Database_Impl.get_db_session() as session:
            # 获取用户所有论文
            limit_start = (int(page_number) - 1) * page_size

            if user_type == 2:
                all_paper = session.query(Paper_Module).filter(Paper_Module.id != 0).limit(page_size).offset(limit_start)
                count = session.query(func.count(Paper_Module.id)).scalar()
            else:
                all_paper = session.query(Paper_Module).filter(Paper_Module.user_id == user_id).limit(page_size).offset(limit_start)
                count = session.query(func.count(Paper_Module.user_id)).filter(Paper_Module.user_id == user_id).scalar()
            for item_paper in all_paper:
                paper = dict()
                paper["id"] = item_paper.id
                paper["name"] = item_paper.name
                paper["number"] = item_paper.number
                paper["key_word"] = item_paper.key_word
                paper["abstract"] = item_paper.abstract
                paper["pdf_path"] = item_paper.pdf_path
                paper["word_path"] = item_paper.word_path
                paper["pdf_name"] = item_paper.pdf_name
                paper["word_name"] = item_paper.word_name
                paper["manage_author_id"] = item_paper.manage_author_id
                paper["manage_author_name"] = str()
                paper["create_date"] = item_paper.create_date
                paper["comments"] = item_paper.comments
                paper["status"] = item_paper.status
                paper["pay_mode"] = item_paper.pay_mode
                paper["money"] = item_paper.money

                # 根据论文ID查找所有作者
                author_list = list()
                all_authors = session.query(Author_Module).filter(Author_Module.paper_id==item_paper.id).all()
                for item_author in all_authors:
                    if item_paper.manage_author_id == item_author.id:
                        paper["manage_author_name"] = item_author.name

                    author = dict()
                    author["id"] = item_author.id
                    author["author_name"] = item_author.name
                    author["english_name"] = item_author.english_name
                    author["org"] = item_author.org
                    author["email"] = item_author.email
                    author["addr"] = item_author.addr
                    author["job_title"] = item_author.job_title
                    author["phone"] = item_author.phone
                    author["wechat"] = item_author.wechat
                    author_list.append(author)

                paper["author_list"] = author_list
                paper_list.append(paper)
            return get_res(data=dict(paperList=paper_list, total=count))

    @classmethod
    @catch_error
    def update_pay(cls, order_no, status, pay_mode):
        with Database_Impl.get_db_session() as session:
            paper = session.query(Paper_Module).filter(Paper_Module.number==order_no).first()
            if paper:
                paper.status = status
                paper.pay_mode = pay_mode
                session.commit()
            return True


class AlipayControl:
    @classmethod
    def go_pay(cls, title, number, money):
        alipay_conf = Conf_Impl.get_alipy_config()
        base64_qr_code = alipay_impl.create_pay(
            subject=title,  # 商品简单描述
            out_trade_no=number,  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
            notify_url=alipay_conf.notify_url,  # 支付成功后通知服务器
            redirect_url=alipay_conf.redirect_url  # 支付成功后跳转的页面
        )
        return base64_qr_code

    @classmethod
    def verify(cls, data: dict, sign):
        try:
            unsigned_item = ordered_dict(data)
            unsigned_str = join_tuple_param(unsigned_item)
            alipay_conf = Conf_Impl.get_alipy_config()
            order_no = data["out_trade_no"].split("-")[0]
            pay_success = rsa_verify_sign(unsigned_str, sign, alipay_conf.ali_key_path, key_is_file=True)
        except Exception as e:
            Lzlog.error("支付包异步验签过程出错: %s data: %s  sign:%s" % (e, data, sign))
        else:
            Order.update_order(pay_success, order_no, "支付宝")


class WeChatPay:
    @classmethod
    def go_pay(cls, title, number, money):
        return wechat_pay.create_pay(title, number, money)

    @classmethod
    def verify(cls, body_xml):
        """
        根据微信支付服务器返回信息，更新订单状态
        :param body_xml:
        :return:
        """
        try:
            key_path = Conf_Impl.get_wechatpay_config()["key_path"]
            with open(key_path, "r") as fp:
                key = fp.read()
            res_dict = xml_to_dict(body_xml)
            sign = res_dict["xml"].pop("sign", None)
            unsigner_item = ordered_dict(deepcopy(res_dict["xml"]))
            unsigner_string = join_tuple_param(unsigner_item) + "&key=" + key
            order_no = res_dict["xml"]["out_trade_no"].split("-")[0]
            my_sign = sign_md5(unsigner_string.encode("utf-8")).upper()
        except Exception as e:
            Lzlog.error("微信验签过程出错: %s  xml: %s" % (e, body_xml))
        else:
            Order.update_order(True if sign == my_sign else False, order_no, "微信")


class Order:
    @classmethod
    def is_pay_success(cls, number):
        """
        查询订单是否支付
        :param number: 订单编号
        :return:
        """
        with Database_Impl.get_db_session() as session:
            paper = session.query(Paper_Module).filter(Paper_Module.number == number).first()
            return True if paper.status == "5" else False


    @classmethod
    def update_order(cls, pay_success, number, mode):
        """
        用来更新指定订单支付装填
        """
        # 支付成功标识
        flag = "5"
        if not pay_success:
            flag = "6"

        try:
            with Database_Impl.get_db_session() as session:
                paper = session.query(Paper_Module).filter(Paper_Module.number==number).first()
                if not paper:
                    Lzlog.error("支付机构：%s -> 未找到订单：%s，状态更改失败!" % (mode, number))
                    return False
                paper.pay_mode = mode
                paper.status = flag
                session.commit()
                Lzlog.error("支付机构：%s -> 订单: %s 已更新为 %s !" % (mode, number, flag))
                return True
        except Exception as e:
            Lzlog.error("支付机构：%s -> 订单: %s 更新过程中出现异常： %s" % (mode, number, e))
            return False


