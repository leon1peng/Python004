# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv


# class SpidersPipeline:
#     def process_item(self, item, spider):


class MaoyannmoviePipeline:
    def __init__(self):
        self.file = open("movies.csv", "a+", encoding="utf-8", newline='')
        self.headers = {"name", "tag", "release"}
        self.writer = csv.DictWriter(self.file, fieldnames=self.headers)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # if item["name"]:
        #     self.writer.writerow([item['name'],item['tag'],item['release']])
        self.writer.writerow(item)
        return item
    
    def close_spider(self, spider):
        self.file.close()
