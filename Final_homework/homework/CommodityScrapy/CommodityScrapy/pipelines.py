# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from .items import CommodityItem, CommentItem
# noinspection PyUnresolvedReferences
from analysis.models import Commodity


class CommodityScrapyPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CommodityItem):
            print("Commodity data")
            item.save()
        elif isinstance(item, CommentItem):
            print("Comments data")
            item.save()
        return item


class CommodityscrapyPipeline:
    def process_item(self, item, spider):
        return item
