"""
数据库初始化
"""
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import contextmanager

from settings.config import Conf_Impl as Conf

pymysql.install_as_MySQLdb()


class Database:
    """
    管理数据库类
    """
    def __init__(self):
        self.db_conf = Conf.get_db_conf()
        self.sql_conf = f'{self.db_conf.type}://{self.db_conf.user}:'
        self.sql_conf += f'{self.db_conf.pad}@{self.db_conf.host}/{self.db_conf.db_name}'
        self.engine = create_engine(self.sql_conf, echo=False)
        self.db_session = sessionmaker(bind=self.engine)
        self.DBBasesClass = declarative_base()

    # 上下文管理装饰器
    @contextmanager
    def get_db_session(self):
        """
        :return: 返回一个带上下文管理的DB操作对象
        """
        session = None
        try:
            session = self.db_session()
            yield session
        except Exception as e:
            if session:
                print("rollback")
                session.rollback()
            raise e
        finally:
            session.close()

    def drop_all(self, t_l):
        if t_l:
            self.DBBasesClass.metadata.drop_all(self.engine, tables=t_l)
        else:
            self.DBBasesClass.metadata.drop_all(self.engine)

    def create_all(self, t_l):
        if t_l:
            self.DBBasesClass.metadata.create_all(self.engine, tables=t_l)
        else:
            self.DBBasesClass.metadata.create_all(self.engine)


# 单利，不用每次使用前需要实例化
Database_Impl = Database()
