import random
import base64
from DoubanTop250.settings import USER_AGENTS
from DoubanTop250.settings import PROXIES
class RandomUserAgent(object):
    def process_request(self,request,spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)

class RandomProxy(object):
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)

        if proxy['user_passwd'] is None:
            request.meta['proxy']="http://" + proxy['ip_port']
        else:
            # 对账户密码进行base64编码转换
            base64_userpasswd = base64.b64encode(bytes(proxy['user_passwd'],'utf-8'))
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = b'Basic ' + base64_userpasswd

            request.meta['proxy'] = "http://" + proxy['ip_port']