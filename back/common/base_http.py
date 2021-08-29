import threading
import datetime
import json
import time
import uuid

from tornado.web import RequestHandler

from common.log import Lzlog
from common.public_mthod import Dict


class UserAuthManager:
    User_Dict = dict()  # key是session  value结构{Login_Time:"",Info:{这里是Manager_Model}}
    Leave_Time = 2 * 60 * 60
    Run_Flag = False  # 线程是否启动

    @staticmethod
    def register(session, userInfo):
        if session not in UserAuthManager.User_Dict:
            UserAuthManager.User_Dict[session] = dict(Login_Time=datetime.datetime.now().timestamp(), Info=userInfo)
        else:
            UserAuthManager.User_Dict[session]['Login_Time'] = datetime.datetime.now().timestamp()

    @staticmethod
    def unregister(session):
        if session in UserAuthManager.User_Dict:
            del UserAuthManager.User_Dict[session]
            return True
        return False

    @staticmethod
    def run():
        if not UserAuthManager.Run_Flag:
            UserAuthManager.Run_Flag = True
            T1 = threading.Thread(target=UserAuthManager.deal_user_state)
            T1.start()

    @staticmethod
    def deal_user_state():
        Lzlog.debug("session有效期检查函数已启动")
        while True:
            Time_Now = datetime .datetime.now().timestamp()
            InValid_Session = []
            for session, v in UserAuthManager.User_Dict.items():
                if (Time_Now - v['Login_Time']) > UserAuthManager.Leave_Time:
                    InValid_Session.append(session)

            for session in InValid_Session:
                if session in UserAuthManager.User_Dict:
                    del UserAuthManager.User_Dict[session]

            time.sleep(5)

    @staticmethod
    def check_session(session):
        return session in UserAuthManager.User_Dict

    @staticmethod
    def get_user_data_from_session(session):
        if session in UserAuthManager.User_Dict:
            return UserAuthManager.User_Dict[session]['Info']
        else:
            return False


class BaseHttp(RequestHandler, UserAuthManager):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE')

    def options(self, *args, **kwargs):
        pass

    def get_current_user(self):
        InData = self.get_data()
        return self.check_session(InData.get('session'))

    def push_session(self, session, user_info):
        self.run()
        self.register(session, user_info)

    def get_user_info(self):
        InData = self.get_data()
        return self.get_user_data_from_session(InData.get('session'))

    def get_data(self):
        """
        将请求过来的参数转为字典对象
        当self.request.body有值的时候需从body取，无值得时候代表使用的get请求，从arguments取值
        """
        InData = dict()
        try:
            if self.request.body.decode() == '':
                for k in self.request.arguments:
                    InData[k] = self.get_argument(k)
            else:
                InData.update(json.loads(self.request.body.decode()))
        except Exception as e:
            try:
                for k in self.request.arguments:
                    InData[k] = self.get_argument(k)
            except Exception as e:
                pass
        return Dict(InData)

    @classmethod
    def gen_session(cls):
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(time.time())))

    @staticmethod
    def get_res(code=0, msg='', data=None):
        return dict(code=code, msg=msg, data=data)

    def _set_para(self):
        self.data = self.get_data()
        self.data.user_info = self.get_user_info()

    def initialize(self) -> None:
        self._set_para()
