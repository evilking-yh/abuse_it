#coding:utf-8
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
import tools.config as config

import jieba

class JiebaTool(object):

    def __init__(self):
        self.stop_words = self._load_dict(config.path_stop_words)

    def _load_dict(self, path):
        return [line.strip() for line in open(path).readlines()]

    def cut(self, line, enable_stop=True):
        ans_list = []

        segs = jieba.cut(line)
        for seg in segs:
            if enable_stop and seg in self.stop_words:
                continue
            ans_list.append(seg)
        return ans_list

jieba_tool = JiebaTool()
if __name__ == '__main__':
    for word in jieba_tool.cut('小米今年二十五岁。'):
        print(word)