import threading
import queue
from lxml import etree
import requests
import json,time,random

#采集线程类
class Crawl(threading.Thread):
    def __init__(self,num,pageQueue,dataQueue):
        #调用Thread父类方法
        super(Crawl,self).__init__()
        #初始化子类属性
        self.num = num
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }

    #线程启动时调用
    def run(self):
        #打印采集线程信息
        print('启动{}号采集线程'.format(self.num))

        #判断请求队列是否为空,不为空无限循环
        while self.pageQueue.qsize() >0:
            url = self.pageQueue.get()
            print('{}号线程采集:{}'.format(self.num,url))

            #防止请求过快,随机设置暂停时间
            time.sleep(random.randint(1,3))

            #发起请求,获取响应内容,追加到数据队列.等待解析
            response = requests.get(url,headers=self.headers)
            if response.status_code == 200:
                self.dataQueue.put(response.text)#向数据队列追加数据,等待解析

#解析线程类
class Parse(threading.Thread):
    def __init__(self,num,dataQueue,pageQueue,f):
        super(Parse,self).__init__()
        self.num=num
        self.dataQueue = dataQueue
        self.pageQueue = pageQueue
        self.f = f
        self.is_parse = True

    def run(self):
        print('启动{}号解析线程'.format(self.num))
        #无限循环
        while True:
            #判断解析线程的结束条件
            for t in self.pageQueue:
                if t.is_alive():
                    break
            else:#如果循环完毕,没有执行break,进入else
                if self.dataQueue.qsize() ==0:
                    self.is_parse=False
            #判断是否继续解析
            if self.is_parse:
                try:
                    data=self.dataQueue.get(timeout=3)
                except Exception as e:
                    data = None
                if data is not None:
                    self.parse(data)
            else:
                break
        print('退出{}号解析线程'.format(self.num))

    #页面解析函数
    def parse(self,data):
        html = etree.HTML(data)
        duanzi_div= html.xpath('//div[@id="content-left"]/div')
        for duanzi in duanzi_div:
            # 获取昵称
            nick = duanzi.xpath('./div//h2/text()')[0]
            nick = nick.replace('\n', '')
            # 获取年龄
            age = duanzi.xpath('.//div[@class="author clearfix"]/div/text()')
            if len(age) > 0:
                age = age[0]
            else:
                age = 0
            # 获取性别
            gender = duanzi.xpath('.//div[@class="author clearfix"]/div/@class')
            if len(gender) > 0:
                if 'women' in gender[0]:
                    gender = '女'
                else:
                    gender = '男'
            else:
                gender = '中'

            # 获取段子内容
            content = duanzi.xpath('.//div[@class="content"]/span[1]/text()')[0].strip()

            # 获取好笑数
            good_num = duanzi.xpath('./div//span[@class="stats-vote"]/i/text()')[0]

            # 获取评论
            common_num = duanzi.xpath('./div//span[@class="stats-comments"]//i/text()')[0]

            item = {
                'nick': nick,
                'age': age,
                'gender': gender,
                'content': content,
                'good_num': good_num,
                'common_num': common_num,
            }

            self.f.write(json.dumps(item,ensure_ascii=False) + '\n')


#===========主函数============
def main():
    #生成请求队列和数据队列,请求以后,响应(response)放入数据队列中
    pageQueue = queue.Queue()
    dataQueue = queue.Queue()

    #创建文件对象
    f = open('duanzi.json','w',encoding='utf-8')

    #循环生成多个请求url
    for i in range(1,14):
        base_url = 'https://www.qiushibaike.com/8hr/page/%d/' % i
        pageQueue.put(base_url)

    #生成N个采集线程
    CrawlList=[]
    for j in range(1,5):
        t = Crawl(j,pageQueue,dataQueue)  #创造线程实例
        t.start()      #运行线程
        CrawlList.append(t)
    #生成N个解析线程
    ParseList=[]
    for k in range(1,5):
        t = Parse(k,dataQueue,CrawlList,f)
        t.start()
        ParseList.append(t)

    for t in CrawlList:
        t.join()
    for t in ParseList:
        t.join()

    #关闭文件对象
    f.close()


if __name__ == '__main__':
    main()