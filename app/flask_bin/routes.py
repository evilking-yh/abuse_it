#coding: utf-8

from flask_bin import app

import json
import base64
import time
import hashlib

from flask import request
from flask import Response
from flask import jsonify
import xml.etree.cElementTree as etree

from tools.config import logger
from tools import utils

from bin.control import chat_control


def pack_msg(code, msg, res=None):
    status = {'code': code, 'message': msg,}

    if res is None:
        msg = {'status': status}
    else:
        msg = {'status': status, 'result': res}

    return msg

def comm_error(status, error):
    message = pack_msg(status, error)
    resp = jsonify(message)
    resp.status_code = status

    logger.warn('handle chat message failed: status=<%d> msg=<%s>'%(status, error))
    return resp

text_str = '''
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
</xml>
'''

img_str = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[%s]]></MediaId></Image></xml>"


image_text_lj = "<ArticleCount>%s</ArticleCount><Articles>%s</Articles></xml>"
image_text_item = "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>"


def reply_muban(type):
    return {'text': text_str, 'image': img_str}.get(type)

def image_text_new_muban(itemDic):

    items = ""
    for item in itemDic:
        items += image_text_item % (item['Title'], item['Description'], item['PicUrl'], item['Url'])

    return '' + (image_text_lj % (len(itemDic), items))


def verify_valid_by_token(data):
    # 这里改写你在微信公众平台里输入的token
    token = 'evilking123'
    # 获取输入参数
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    echostr = data.get('echostr', '')
    # 字典排序
    list = [token, timestamp, nonce]
    list.sort()

    s = list[0] + list[1] + list[2]
    # sha1加密算法
    hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
    # 如果是来自微信的请求，则回复echostr
    if hascode == signature:
        return echostr
    else:
        return ""

def chat_msg(msg):
    res_msg, chat_time = chat_control.handle(msg)

    return res_msg

@app.route('/chat_it', methods=['GET','POST'])
def parse():
    if request.method == 'GET':
        return verify_valid_by_token(request.args)

    if request.method == 'POST':
        str_xml = request.stream.read()
        xml = etree.fromstring(str_xml)
        msgType = xml.find("MsgType").text
        xml_muban = reply_muban(msgType)
        if msgType == 'text':
            content = xml.find("Content").text
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            return xml_muban % (fromUser, toUser, int(time.time()), chat_msg(content))
        elif msgType == 'image':
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            mediaid = xml.find("MediaId").text
            print(xml_muban % (fromUser, toUser, int(time.time()), mediaid))
            return xml_muban % (fromUser, toUser, int(time.time()), mediaid)
        else:
            itemDic = [{'Title': 'Title', 'Description': 'Description',
                        'PicUrl': 'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                        'Url': 'www.baidu.com'}, {'Title': 'Title1', 'Description': 'Description1',
                                                  'PicUrl': 'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                                                  'Url': 'www.baidu.com'}]
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            mediaid = xml.find("MediaId").text
            return image_text_new_muban(itemDic) % (fromUser, toUser, int(time.time()))


@app.route('/chat_it_bak', methods=['POST'])
def parse_bak():
    '''
    fname: 文件名
    content: 文件内容
    '''
    t_start = time.time()

    data = request.data
    js = json.loads(data)

    name = js.get('name', '')
    message_cont_b64 = js.get('content', '')
    req_time = js.get('time', '')

    logger.info('receive chat message request: name=<%s>'%(name))

    msg = base64.b64decode(message_cont_b64)
    msg = msg.decode('utf-8')

    res_msg, chat_time = chat_control.handle(msg, name, req_time)

    res = utils.jsonify(name, res_msg, chat_time)
    js = pack_msg(200, 'success', res)
    js = json.dumps(js)

    resp = Response(js, status=200, mimetype='application/json')

    logger.info('handle chat message finished: name=<%s>, cost <%d> ms' % (name, int((time.time() - t_start) * 1000)))

    return resp
