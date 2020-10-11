# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

import pymysql


# class SpidersPipeline:
#     def process_item(self, item, spider):


class MysqlPipeline(object):
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123',
            db='test1',
            charset='utf8mb4'
        )
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = "insert into movies(release,name,tag) VALUES(%s,%s,%s)"
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['release'], item['name'], item['tag']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
