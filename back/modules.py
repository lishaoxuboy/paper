"""
数据库模型
"""
from sqlalchemy import String, Integer, Column, Text, ForeignKey
from common.database import Database_Impl


class User_Module(Database_Impl.DBBasesClass):
    """

    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), comment="名字")
    account = Column(String(255), comment="账号")
    password = Column(String(255), comment="密码")
    email_addr = Column(String(255), comment="邮箱地址")
    role = Column(String(1), default="1")


class Paper_Module(Database_Impl.DBBasesClass):
    """
    论文
    """
    __tablename__ = "paper"

    # 论文的基础信息
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), comment="论文名字")
    number = Column(String(255), comment="论文编号")
    key_word = Column(String(255), comment="论文关键字")
    abstract = Column(String(255), comment="论文关摘要")
    pdf_path = Column(String(255), comment="上传的论文的pdf")
    word_path = Column(String(255), comment="上传的论文的word")
    pdf_name = Column(String(255), comment="pdf文件名字")
    word_name = Column(String(255), comment="word文档名字")
    manage_author_id = Column(Integer, comment="管理改论文的作者，作者可能有多个")
    user_id = Column(Integer, comment="改论文所属的用户ID")
    create_date = Column(String(255), comment="创建日期")

    # 管理员可以对改论文提出修改建议
    comments = Column(String(255), comment="管理员提出的建议")
    status = Column(String(128), comment="状态 1：未批注 2: 已批注 3: 被采纳（也就是'待付款'）  4：已拒稿 5:已付款 ", default=1)
    money = Column(String(255), comment="订单金额")

    # 一个论文也是一个订单 当论文被采纳时候，它就是一个订单了 jin'e
    pay_mode = Column(String(128), comment="付款方式")


class Author_Module(Database_Impl.DBBasesClass):
    """
    作者
    """
    __tablename__ = "auther"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), comment="作者名字")
    english_name = Column(String(255), comment="作者英文名")
    org = Column(String(255), comment="单位")
    email = Column(String(255), comment="工作邮箱")
    addr = Column(String(255), comment="联系地址")

    job_title = Column(String(255), comment="职称")
    phone = Column(String(128), comment="联系方式")
    wechat = Column(String(255), comment="微信")
    paper_id = Column(Integer, comment="作者关联的论文id")
