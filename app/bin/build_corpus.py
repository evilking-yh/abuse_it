#coding:utf-8
import sys
import os, re
from os.path import dirname, abspath, join
sys.path.append(dirname(dirname(abspath(__file__))))
from bs4 import BeautifulSoup

import tools.config as config


path_root = dirname(dirname(__file__))
original_data_path = join(dirname(path_root), 'data/')

print(original_data_path)

dirty_pat = re.compile('[骂脏恶丑贱淫]')
clear_pat = re.compile('^[\d,、，. ]+')
lines_set = set()
def scan_corpus(dir_path):
    if not os.path.exists(dir_path):
        print('not found %s' % dir_path)
        return
    names = os.listdir(dir_path)
    for name in names:
        if name == '.DS_Store':
            continue
        file_path = join(dir_path, name)
        if os.path.isdir(file_path):
            scan_corpus(file_path)
        else:
            with open(file_path, 'r') as fr:
                temp_lines = fr.readlines()
                for li, line in enumerate(temp_lines):
                    if li == 0 and not dirty_pat.search(line):
                        break
                    elif li > 0 and line.strip() != '':
                        soup = BeautifulSoup(line, 'lxml')
                        line = soup.get_text().strip()
                        line = clear_pat.sub('', line)
                        lines_set.add(line + '\n')

scan_corpus(original_data_path)

fw = open(config.path_dirty_talk, 'w')
fw.writelines(list(lines_set))
fw.flush()
fw.close()