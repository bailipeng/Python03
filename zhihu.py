from bs4 import BeautifulSoup
import requests
import time

def captcha(captcha_data):
    #将验证码保存成jpg格式
    with open('captcha.jpg','wb') as f:
        f.write(captcha_data)
    #打开保存的图片,输入验证码
    captcha = input('请输入验证码:')
    #返回输入的验证码
    return captcha



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
    print(res.text)

if __name__ == '__main__':
    zhihuLogin()