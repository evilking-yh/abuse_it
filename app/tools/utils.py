#coding: utf8
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import os
import io


def jsonify(name, res_msg, chat_time):
    js = {}

    js['name'] = name
    js['content'] = res_msg
    js['time'] = chat_time

    return js

def get_file_info(path):
    (filepath, tempfilename) = os.path.split(path)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension


def line_generator(fname):
    '''产生器：从文件中读取line'''

    lno = 0
    for line in io.open(fname):
        if lno == 0 and len(line) > 0 and line[0] == u'\ufeff':
            line = line[1:]
        lno += 1

        yield line.strip()

def clear_file(path):
    if os.path.exists(path):
        os.remove(path)
