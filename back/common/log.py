import os
import time
import logging.handlers


class CreateLog(object):

    def __init__(self):
        self.dir_path = os.path.join(os.getcwd(), "log")
        self.info_path = os.path.join(self.dir_path, "info")
        self.err_path = os.path.join(self.dir_path, "error")
        self.log_format = "%(asctime)s - %(levelname)s: %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.make_dir()

    def make_dir(self):
        if os.path.exists(self.dir_path) and os.path.isdir(self.dir_path):
            if os.path.exists(self.info_path):
                pass
            else:
                os.mkdir(self.info_path)
            if os.path.exists(self.err_path):
                pass
            else:
                os.mkdir(self.err_path)
        else:
            os.mkdir(self.dir_path)
            os.mkdir(self.info_path)
            os.mkdir(self.err_path)

    def create_log(self):
        error_log_name = (time.strftime("error-%Y%m%d", time.localtime())) + ".log"
        info_log_name = (time.strftime("info-%Y%m%d", time.localtime())) + ".log"
        error_path = os.path.join(self.err_path, error_log_name)
        info_path = os.path.join(self.info_path, info_log_name)
        logging.basicConfig(level=logging.DEBUG, format=self.log_format, datefmt=self.date_format)

        logger = logging.getLogger('Lzlog')

        handler = logging.handlers.RotatingFileHandler(filename=error_path, maxBytes=50 * 1024 * 1024, backupCount=7,
                                                       encoding="utf-8", delay=False)
        fmt = logging.Formatter(fmt=self.log_format)
        handler.setFormatter(fmt)
        handler2 = logging.handlers.RotatingFileHandler(filename=info_path, maxBytes=50 * 1024 * 1024, backupCount=7,
                                                        encoding="utf-8", delay=False)
        fmt = logging.Formatter(fmt=self.log_format)
        handler2.setFormatter(fmt)

        handler.setLevel(logging.ERROR)
        handler2.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.addHandler(handler2)
        return logger


Lzlog = CreateLog().create_log()