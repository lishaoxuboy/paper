import threading
import os

import smtplib
from email.mime.text import MIMEText  # 导入 MIMEText 类
from email.mime.multipart import MIMEMultipart  # 导入MIMEMultipart类
from email.mime.image import MIMEImage  # 导入MIMEImage类
from email.mime.base import MIMEBase  # MIME子类的基类
from email import encoders  # 导入编码器
from email.header import Header

from common.log import Lzlog


class SendEmail:
    """发送邮件"""
    def __init__(self,code, minute, operation, email_format, file_name=None, audio_name=None, to_address="lz13817623252@163.com", from_address="lz13817623252@163.com", from_pwd="lz8888"):
        self.HOST = "smtp.163.com"  # 定义 smtp 主机
        self.PORT = "25"            # 发送端口 统一指定25
        self.SUBJECT = Header('欢迎注册', 'utf-8').encode()  # 定义邮件主题
        self.TO = to_address  # 定义邮件收件人
        self.FROM = from_address  # 定义邮件发件人
        self.PWD = from_pwd
        self.Code = code
        self.Minute = minute
        self.Filename = file_name
        self.Audioname = audio_name
        self.operation = operation
        self.email_format = email_format
        self.__init()

    def __init(self):
        self.msg = MIMEMultipart('related')  # 创建MIMEMultipart对象，采用related定义内嵌资源邮件体
        # self.__html_img()
        # if self.Filename and os.path.exists(self.Filename):
        #     self.__file_img(self.Filename)
        # if self.Audioname and os.path.exists(self.Audioname):
        #     self.__file_img(self.Audioname)
        self.__html_img()
        t1 = threading.Thread(target=self.__to_email)
        t1.start()

    def __addimg(self, img_id):  # 定义图片读取函数，参数1为图片路径，2为图片ID机标识符
        with open(self.Filename, 'rb') as f:
            msgimage = MIMEImage(f.read())  # 读取图片内容
        msgimage.add_header('Content-ID', img_id)  # 指定文件的Content-ID,<img>,在HTML中图片src将用到

        return msgimage

    def __html_img(self):
        # 创建一个MIMEText对象，HTML元素包括文字与图片
        # msgtext = MIMEText("<font color=red> 给你一个大大的爱心 :<br><img src=\"cid:weekly\"border=\"1\"><br>。</font>", "html", "utf-8")
        # content = self.email_format % (self.operation, self.Code, self.Minute)
        content = self.email_format.replace("&OPERATION&", self.operation).replace("&CODE&", str(self.Code)).replace("&MINUTE&", str(self.Minute))
        msgtext = MIMEText(content, "html", "utf-8")
        self.msg.attach(msgtext)  # 将msgtext内容附加到MIMEMultipart对象中
        # self.msg.attach(self.__addimg('weekly'))  # 使用MIMEMultipart对象附加MIMEImage的内容

    # 附件文件定义
    # 创建一个MIMEText对象，附加表格文件（week.xlsx）
    def __file_img(self, filename):
        attachfile = MIMEBase('applocation', 'octet-stream')  # 创建对象指定主要类型和次要类型
        attachfile.set_payload(open(filename, 'rb').read())  # 将消息内容设置为有效载荷
        attachfile.add_header('Content-Disposition', 'attachment', Filename=('utf-8', '', filename))  # 扩展标题设置
        encoders.encode_base64(attachfile)
        self.msg.attach(attachfile)  # 附加对象加入到msg

    def __to_email(self):
        self.msg['Subject'] = self.SUBJECT  # 邮件主题
        self.msg['from'] = self.FROM  # 邮件发件人 , 邮件头部可见
        self.msg['to'] = self.TO  # 邮件收件人 , 邮件头部可见
        try:
            server = smtplib.SMTP()  # 创建一个 SMTP() 对象
            server.connect(self.HOST, self.PORT)  # 通过 connect 方法连接 smtp 主机
            server.starttls()  # 启动安全传输模式

            server.login(self.FROM, self.PWD)  # 邮箱账号登录校验
            server.sendmail(self.FROM, self.TO, self.msg.as_string())  # 邮件发送
            server.quit()  # 断开 smtp 连接
            Lzlog.info("发送邮件到 %s 成功！" % self.TO)
        except Exception as e:
            Lzlog.info("发送邮件到 %s 失败：%s" % (self.TO, e))


def send_email(to, code, minute, operation):
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/email.html")
        with open(path, "r", encoding="utf-8") as fp:
            email_format = fp.read()
            SendEmail(to_address=to, code=code, minute=minute, operation=operation, email_format=email_format)
            return True
    except Exception as e:
        Lzlog.error("发送 %s 邮件错误 %s" % (to, e))
        return False


if __name__ == '__main__':
    send_email("sunnylishaoxu@163.com", 1002, 3, "注册账号")
