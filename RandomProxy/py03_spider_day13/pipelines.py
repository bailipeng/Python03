# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Py03SpiderDay13Pipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1','root','123456','temp',charset='utf8')
        self.cursor = self.conn.cursor()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

class XiciMysqlPipeline(MysqlPipeline):
    def process_item(self,item, spider):
        if spider.name == 'xici':
            sql = 'insert into proxy_gaoni(host,port,http_type) ' \
                  'VALUES(%s,%s,%s) on duplicate key update port=values(port),http_type=VALUES(http_type)'
            try:
                self.cursor.execute(sql,(item['host'],item['port'],item['http_type']))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                print(e)
                print('执行语句失败')
            # 返回交给下一个管道文件处理
        return item