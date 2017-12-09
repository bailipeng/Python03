# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Doubantop250Pipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1','root','123456','bai',charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into DoubanTop(title,bd,star,quote) VALUES ("%s","%s","%s","%s") '%(item['title'], item['bd'], item['star'], item['quote'])
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('执行语句失败',e)
        return item


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用