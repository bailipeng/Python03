# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql,json


class TententPipeline(object):
    def __init__(self):
        # 可选实现，做参数初始化等
        # doing something
        pass
    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，

        #使用pymysql 链接数据库
        conn = pymysql.connect('127.0.0.1','root','123456','bai',charset='utf8')
        #制作一个游标,操作数据
        cursor = conn.cursor()
        #写好sql语句
        sql = 'insert into TencentForm(name,detailLink,positionInfo,peopleNumber,workLocation,publishTime) VALUES ("%s","%s","%s","%s","%s","%s")' % (item['name'], item['detailLink'], item['positionInfo'], item['peopleNumber'], item['workLocation'],item['publishTime'])
        #执行sql语句写入数据库
        cursor.execute(sql)
        #提交事务,使其生效
        conn.commit()
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
        return item



    def open_spider(self, spider):
        pass
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。

    def close_spider(self, spider):
        pass
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用