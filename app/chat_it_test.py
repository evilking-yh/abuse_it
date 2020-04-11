#coding: utf-8

import requests
import json
import base64
import sys
import os
import time

# print(sys.argv)
# if len(sys.argv) < 3:
#     print("warring: parameter incompleteness, using default config!!! ")
#     print("help: command corpus_path n_gram")
#     print("e.g.: python app/bin/join_line_test.py /Users/hulk/forindo/join_line/data/cn_test.txt 3")
#
#     sys.exit()
#
# filename = sys.argv[1]
# n_gram = sys.argv[2]

name = 'hulk'
# msg = '我日你妈，你个小逼崽子'


# content = base64.b64encode(msg.encode('utf-8')).decode('utf-8')

xmldata = '''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>'''

data = {
	'content': content,
	'name': name,
	'time': time.time()
}
response = requests.post(
	'http://%s:80/chat_it' % '182.254.232.98',
	data=json.dumps(data),
	)
if response.status_code == 200:
	result = response.json()

	print(json.dumps(result, indent=2, ensure_ascii=False))
else:
	print(response.text)
	print('Error response. please check')

