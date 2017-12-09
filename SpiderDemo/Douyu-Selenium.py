import unittest
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
class Douyu(unittest.TestCase):
    #初始化方法,固定写法setUp()
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.num = 0
        self.total = 0


    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            #用获取到的源码作为原料,熬一锅美丽汤
            soup = bs(self.driver.page_source,'lxml')

            #房间名,返回的是列表
            names = soup.find_all("h3", {"class" : "ellipsis"})
            #观众人数,返回的是列表
            nums = soup.find_all("span", {"class" :"dy-num fr"})

            #zip()将两个列表合成一个元组
            for name,num in zip(names,nums):
                print('观众人数: '+num.get_text().strip() + u"-\t房间名: " + name.get_text().strip())
                self.num +=1
                numstr = num.get_text().strip()
                if '万' in numstr:
                    numint = float(numstr.replace('万',''))*10000
                else:
                    numint = int(numstr)

                self.total += numint


            #退出条件
            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                break

            #重点,重复点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()
            time.sleep(1)

    #测试结束执行方法
    def tearDown(self):
        #退出PhantomJS()浏览器
        print("当前网站直播人数:"+str(self.num))
        print("总计观看人数:"+str(self.total))
        self.driver.quit()

if __name__ == '__main__':
    #启动测试模块
    unittest.main()