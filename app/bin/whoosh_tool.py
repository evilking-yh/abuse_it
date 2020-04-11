#coding:utf-8

import sys
import os, shutil
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
import tools.config as config
from bin.jieba_tool import jieba_tool

from whoosh import fields
from whoosh import index
from whoosh.qparser import QueryParser


class WhooshTool(object):

    def __init__(self):
        if not os.path.exists(config.path_index):
            self.build_index()

    def build_index(self):
        schema = fields.Schema(keyword=fields.TEXT(stored=True), content=fields.TEXT(stored=True))

        if not os.path.exists(config.path_index):
            os.mkdir(config.path_index)
        else:
            shutil.rmtree(config.path_index)
            os.mkdir(config.path_index)

        index.create_in(config.path_index, schema)
        ix = index.open_dir(config.path_index)

        writer = ix.writer()

        with open(config.path_dirty_talk, 'r') as fr:
            for line in fr:
                for word in jieba_tool.cut(line):
                    print(word)
                    writer.add_document(keyword=word, content=line.strip())

        writer.commit()

    def search_hit(self, keyword):
        ans_list = []

        ix = index.open_dir(config.path_index)
        with ix.searcher() as searcher:
            query = QueryParser('keyword', ix.schema).parse(keyword)
            result = searcher.search(query)
            for res in result:
                ans_list.append(dict(res))

        return ans_list

whoosh_tool = WhooshTool()
if __name__ == '__main__':
    whoosh_tool.search_hit('崽子')


