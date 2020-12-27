# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
# noinspection PyUnresolvedReferences
from analysis import models


class CommodityItem(DjangoItem):
    django_model = models.Commodity


class CommentItem(DjangoItem):
    django_model = models.Comments
