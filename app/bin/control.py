#coding:utf-8
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import time
from bin.jieba_tool import jieba_tool
from bin.whoosh_tool import whoosh_tool

class ChatControl(object):

    def __init__(self):
        pass

    def handle(self, msg, name='', req_time=''):
        ans_list = []

        words = jieba_tool.cut(msg)
        for word in words:
            candidate_ans = whoosh_tool.search_hit(word)
            for cand in candidate_ans:
                ans_list.append(cand['content'])

        return '\n'.join(ans_list), time.time()

chat_control = ChatControl()

if __name__ == '__main__':
    ans = chat_control.handle('hulk', '我日你妈，你个小逼崽子', '')
    for ans_str in ans:
        print(ans_str)