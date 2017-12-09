from bs4 import BeautifulSoup
import requests
import time
from pytesseract import *  #注意配置好环境变量
from PIL import Image
import json

def captcha(captcha_data):
    #将验证码保存成jpg格式
    with open('captcha.jpg','wb') as f:
        f.write(captcha_data)

    #此处暂停1s ,使图片加载完成
    time.sleep(1)
    #将图片打开,返回一个image对象
    image=Image.open('captcha.jpg')
    #使用tesseract将图片识别为字符串
    text = image_to_string(image)
    #打印识别的字符串,与保存的图片核对
    print('识别的验证码为:'+text)
    #确定是否可用,不可用的话......手动输入吧!也可以写个循环直到识别对为止!
    while True:
        command = input('确定/手动(y/n):')
        if command == 'y' or command == 'Y':
            return text
        elif command == 'n' or command == 'N':
            return input('请输入验证码:')
        else:
            continue


def zhihuLogin():
    #构建session对象,保存cookie
    sess = requests.session()
    #构建headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    #获取登录页面html
    html = sess.get('https://www.zhihu.com/#signin',headers=headers).text
    #熬一锅美丽汤
    bs = BeautifulSoup(html,'lxml')
    #用勺子提取_xsrf的值(动态生成,防止跨越攻击的字段)
    _xsrf = bs.find('input',attrs={'name':'_xsrf'}).get('value')
    #生成验证码的url地址
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login"%(time.time()*1000)
    #获取验证码图片的二进制数据内容
    captcha_data = sess.get(captcha_url,headers=headers).content
    #获取验证码(通过captcha函数)
    text = captcha(captcha_data)
    #构建post请求需要的data数据(form表单)
    data = {
        '_xsrf': _xsrf,
        'phone_num':'手机号',#注意如果用email登录,字段是email:'邮箱名',同时post提交地址也要改为login/email
        'password':'密码',
        'captcha':text
    }
    #发送post请求
    res = sess.post('https://www.zhihu.com/login/phone_num',data=data,headers=headers)
    #打印出请求结果,返回'登录成功'即可为所欲为了
    print(json.loads(res.text))

if __name__ == '__main__':
    zhihuLogin()