#coding: utf-8

import os
import datetime
import logging
import configparser
from os.path import dirname

def get_package_root():
  return dirname(__file__)

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

path_root = dirname(get_package_root())
conf_path = os.path.join(path_root, 'conf/app_config.conf')

config = configparser.ConfigParser()
config.read(conf_path)

module_name = config.get('global', 'module_name')

path_log = os.path.join(path_root, config.get('global', 'log_path'))
path_stop_words = os.path.join(path_root, config.get('global', 'stop_word_path'))

path_corpus = os.path.join(path_root, config.get('data', 'corpus_path'))
path_dirty_talk = os.path.join(path_root, config.get('data', 'dirty_talk_path'))
path_index = os.path.join(path_root, config.get('data', 'index_path'))

create_path(path_log)
assert os.path.isdir(path_log)
create_path(path_corpus)
assert os.path.isdir(path_corpus)

class LevelFilter(logging.Filter):

    def __init__(self, min_level, max_level):
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, rec):
        if rec.levelno >= self.min_level and rec.levelno <= self.max_level:
            return 1
        return 0


def _get_log_file(name):
    log_file = os.path.join(path_log, name + '.log')
    date = str(datetime.datetime.now())[:10]
    no = 0
    while True:
        no += 1
        fname = '%s.%s.%d' % (log_file, date, no)
        if not os.path.exists(fname):
            break

    # fname = '%s.%s.%d' % (log_file, date, no)
    fname = '%s.%s' % (log_file, date)
    return fname


def _get_logger(name):
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] '
                                      '[%(filename)s:%(lineno)d] [%(message)s]')

    log_file = _get_log_file(name)
    # sys.stderr.write('logging to: %s\n' % (log_file,))
    # sys.stderr.flush()

    # 正常日志
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    handler.addFilter(LevelFilter(logging.DEBUG, logging.INFO))

    # 异常日志
    log_file_wf = log_file + '.wf'
    handler_wf = logging.FileHandler(log_file_wf)
    handler_wf.setFormatter(formatter)
    handler_wf.setLevel(logging.WARNING)

    # 控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(handler_wf)
    logger.addHandler(console)

    return logger


logger = _get_logger(module_name)
logger.info('configurations setup ok')