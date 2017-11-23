#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
 
import os
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
 
try:
    import urllib2 as wdf_urllib
    from cookielib import CookieJar
except ImportError:
    import urllib.request as wdf_urllib
    from http.cookiejar import CookieJar
 
import re
import time
import xml.dom.minidom
import json
import sys
import math
import subprocess
import ssl
 
DEBUG = False
 
MAX_GROUP_NUM = 35  # 每组人数
INTERFACE_CALLING_INTERVAL = 16  # 接口调用时间间隔, 值设为13时亲测出现"操作太频繁"
MAX_PROGRESS_LEN = 50
 
QRImagePath = os.path.join(os.getcwd(), 'qrcode.jpg')
 
tip = 0
uuid = ''
 
base_uri = ''
redirect_uri = ''
 
skey = ''
wxsid = ''
wxuin = ''
pass_ticket = ''
deviceId = 'e000000000000000'
 
BaseRequest = {}
 
ContactList = []
My = []
SyncKey = ''
 
try:
    xrange
    range = xrange
except:
    # python 3
    pass
 
def getRequest(url, data=None):
    try:
        data = data.encode('utf-8')
    except:
        pass
    finally:
        return wdf_urllib.Request(url=url, data=data)
 
def getUUID():
    global uuid
 
    url = 'https://login.weixin.qq.com/jslogin'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time()),
    }
 
    request = getRequest(url=url, data=urlencode(params))
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    # window.QRLogin.code = 200; window.QRLogin.uuid = "oZwt_bFfRg==";
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)
 
    code = pm.group(1)
    uuid = pm.group(2)
 
    if code == '200':
        return True
 
    return False
 
def showQRImage():
    global tip
 
    url = 'https://login.weixin.qq.com/qrcode/' + uuid
    params = {
        't': 'webwx',
        '_': int(time.time()),
    }
 
    request = getRequest(url=url, data=urlencode(params))
    response = wdf_urllib.urlopen(request)
 
    tip = 1
 
    f = open(QRImagePath, 'wb')
    f.write(response.read())
    f.close()
 
    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', QRImagePath])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', QRImagePath])
    else:
        os.startfile(QRImagePath)
 
    print('请使用微信扫描二维码以登录')
 
def waitForLogin():
    global tip, base_uri, redirect_uri
 
    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
        tip, uuid, int(time.time()))
 
    request = getRequest(url=url)
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    # window.code=500;
    regx = r'window.code=(\d+);'
    pm = re.search(regx, data)
 
    code = pm.group(1)
 
    if code == '201':  # 已扫描
        print('成功扫描,请在手机上点击确认以登录')
        tip = 0
    elif code == '200':  # 已登录
        print('正在登录...')
        regx = r'window.redirect_uri="(\S+?)";'
        pm = re.search(regx, data)
        redirect_uri = pm.group(1) + '&fun=new'
        base_uri = redirect_uri[:redirect_uri.rfind('/')]
 
        # closeQRImage
        if sys.platform.find('darwin') >= 0:  # for OSX with Preview
            os.system("osascript -e 'quit app \"Preview\"'")
    elif code == '408':  # 超时
        pass
    # elif code == '400' or code == '500':
 
    return code
 
def login():
    global skey, wxsid, wxuin, pass_ticket, BaseRequest
 
    request = getRequest(url=redirect_uri)
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    '''
        <error>
            <ret>0</ret>
            <message>OK</message>
            <skey>xxx</skey>
            <wxsid>xxx</wxsid>
            <wxuin>xxx</wxuin>
            <pass_ticket>xxx</pass_ticket>
            <isgrayscale>1</isgrayscale>
        </error>
    '''
 
    doc = xml.dom.minidom.parseString(data)
    root = doc.documentElement
 
    for node in root.childNodes:
        if node.nodeName == 'skey':
            skey = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            wxsid = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            wxuin = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            pass_ticket = node.childNodes[0].data
 
    # print('skey: %s, wxsid: %s, wxuin: %s, pass_ticket: %s' % (skey, wxsid,
    # wxuin, pass_ticket))
 
    if not all((skey, wxsid, wxuin, pass_ticket)):
        return False
 
    BaseRequest = {
        'Uin': int(wxuin),
        'Sid': wxsid,
        'Skey': skey,
        'DeviceID': deviceId,
    }
 
    return True
 
def webwxinit():
 
    url = base_uri + \
        '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time()))
    params = {
        'BaseRequest': BaseRequest
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read()
 
    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxinit.json'), 'wb')
        f.write(data)
        f.close()
 
    data = data.decode('utf-8', 'replace')
 
    # print(data)
 
    global ContactList, My, SyncKey
    dic = json.loads(data)
    ContactList = dic['ContactList']
    My = dic['User']
 
    SyncKeyList = []
    for item in dic['SyncKey']['List']:
        SyncKeyList.append('%s_%s' % (item['Key'], item['Val']))
    SyncKey = '|'.join(SyncKeyList)
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    Ret = dic['BaseResponse']['Ret']
    if Ret != 0:
        return False
 
    return True
 
def webwxgetcontact():
 
    url = base_uri + \
        '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time()))
 
    request = getRequest(url=url)
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read()
 
    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxgetcontact.json'), 'wb')
        f.write(data)
        f.close()
 
    # print(data)
    data = data.decode('utf-8', 'replace')
 
    dic = json.loads(data)
    MemberList = dic['MemberList']
 
    # 倒序遍历,不然删除的时候出问题..
    SpecialUsers = ["newsapp", "fmessage", "filehelper", "weibo", "qqmail", "tmessage", "qmessage", "qqsync", "floatbottle", "lbsapp", "shakeapp", "medianote", "qqfriend", "readerapp", "blogapp", "facebookapp", "masssendapp",
                    "meishiapp", "feedsapp", "voip", "blogappweixin", "weixin", "brandsessionholder", "weixinreminder", "wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c", "officialaccounts", "notification_messages", "wxitil", "userexperience_alarm"]
    for i in range(len(MemberList) - 1, -1, -1):
        Member = MemberList[i]
        if Member['VerifyFlag'] & 8 != 0:  # 公众号/服务号
            MemberList.remove(Member)
        elif Member['UserName'] in SpecialUsers:  # 特殊账号
            MemberList.remove(Member)
        elif Member['UserName'].find('@@') != -1:  # 群聊
            MemberList.remove(Member)
        elif Member['UserName'] == My['UserName']:  # 自己
            MemberList.remove(Member)
 
    return MemberList
 
def createChatroom(UserNames):
    # MemberList = []
    # for UserName in UserNames:
        # MemberList.append({'UserName': UserName})
    MemberList = [{'UserName': UserName} for UserName in UserNames]
 
    url = base_uri + \
        '/webwxcreatechatroom?pass_ticket=%s&r=%s' % (
            pass_ticket, int(time.time()))
    params = {
        'BaseRequest': BaseRequest,
        'MemberCount': len(MemberList),
        'MemberList': MemberList,
        'Topic': '',
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    ChatRoomName = dic['ChatRoomName']
    MemberList = dic['MemberList']
    DeletedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:  # 被对方删除了
            DeletedList.append(Member['UserName'])
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    return ChatRoomName, DeletedList
 
def deleteMember(ChatRoomName, UserNames):
    url = base_uri + \
        '/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'DelMemberList': ','.join(UserNames),
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    ErrMsg = dic['BaseResponse']['ErrMsg']
    Ret = dic['BaseResponse']['Ret']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (Ret, ErrMsg))
 
    if Ret != 0:
        return False
 
    return True
 
def addMember(ChatRoomName, UserNames):
    url = base_uri + \
        '/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'AddMemberList': ','.join(UserNames),
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    MemberList = dic['MemberList']
    DeletedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:  # 被对方删除了
            DeletedList.append(Member['UserName'])
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    return DeletedList
 
def syncCheck():
    url = base_uri + '/synccheck?'
    params = {
        'skey': BaseRequest['SKey'],
        'sid': BaseRequest['Sid'],
        'uin': BaseRequest['Uin'],
        'deviceId': BaseRequest['DeviceID'],
        'synckey': SyncKey,
        'r': int(time.time()),
    }
 
    request = getRequest(url=url + urlencode(params))
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    # window.synccheck={retcode:"0",selector:"2"}
 
def main():
 
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
 
        opener = wdf_urllib.build_opener(
            wdf_urllib.HTTPCookieProcessor(CookieJar()))
        wdf_urllib.install_opener(opener)
    except:
        pass
 
    if not getUUID():
        print('获取uuid失败')
        return
 
    showQRImage()
    time.sleep(1)
 
    while waitForLogin() != '200':
        pass
 
    os.remove(QRImagePath)
 
    if not login():
        print('登录失败')
        return
 
    if not webwxinit():
        print('初始化失败')
        return
 
    MemberList = webwxgetcontact()
 
    MemberCount = len(MemberList)
    print('通讯录共%s位好友' % MemberCount)
 
    ChatRoomName = ''
    result = []
    d = {}
    for Member in MemberList:
        d[Member['UserName']] = (Member['NickName'].encode(
            'utf-8'), Member['RemarkName'].encode('utf-8'))
    print('开始查找...')
    group_num = int(math.ceil(MemberCount / float(MAX_GROUP_NUM)))
    for i in range(0, group_num):
        UserNames = []
        for j in range(0, MAX_GROUP_NUM):
            if i * MAX_GROUP_NUM + j >= MemberCount:
                break
            Member = MemberList[i * MAX_GROUP_NUM + j]
            UserNames.append(Member['UserName'])
 
        # 新建群组/添加成员
        if ChatRoomName == '':
            (ChatRoomName, DeletedList) = createChatroom(UserNames)
        else:
            DeletedList = addMember(ChatRoomName, UserNames)
 
        DeletedCount = len(DeletedList)
        if DeletedCount > 0:
            result += DeletedList
 
        # 删除成员
        deleteMember(ChatRoomName, UserNames)
 
        # 进度条
        progress_len = MAX_PROGRESS_LEN
        progress = '-' * progress_len
        progress_str = '%s' % ''.join(
            map(lambda x: '#', progress[:(progress_len * (i + 1)) / group_num]))
        print(''.join(
            ['[', progress_str, ''.join('-' * (progress_len - len(progress_str))), ']']))
        print('新发现你被%d人删除' % DeletedCount)
        for i in range(DeletedCount):
            if d[DeletedList[i]][1] != '':
                print(d[DeletedList[i]][0] + '(%s)' % d[DeletedList[i]][1])
            else:
                print(d[DeletedList[i]][0])
 
        if i != group_num - 1:
            print('正在继续查找,请耐心等待...')
            # 下一次进行接口调用需要等待的时间
            time.sleep(INTERFACE_CALLING_INTERVAL)
    # todo 删除群组
 
    print('\n结果汇总完毕,20s后可重试...')
    resultNames = []
    for r in result:
        if d[r][1] != '':
            resultNames.append(d[r][0] + '(%s)' % d[r][1])
        else:
            resultNames.append(d[r][0])
 
    print('---------- 被删除的好友列表(共%d人) ----------' % len(result))
    # 过滤emoji
    resultNames = map(lambda x: re.sub(r'<span.+/span>', '', x), resultNames)
    if len(resultNames):
        print('\n'.join(resultNames))
    else:
        print("无")
    print('---------------------------------------------')
 
# windows下编码问题修复
# http://blog.csdn.net/heyuxuanzee/article/details/8442718
 
class UnicodeStreamFilter:
 
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding
 
    def write(self, s):
        if type(s) == str:
            s = s.decode('utf-8')
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)
 
if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)
 
if __name__ == '__main__':
 
    print('本程序的查询结果可能会引起一些心理上的不适,请小心使用...')
    print('开始')
    main()
    print('结束')