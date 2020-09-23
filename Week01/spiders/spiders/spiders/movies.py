import scrapy
from scrapy import Request
from scrapy.selector import Selector
from lxml import etree
from ..items import MaoyanmoiveItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']
    
    def start_requests(self):
        url = "https://maoyan.com/films?showType=3"
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取所有的电影信息
        html = etree.HTML(response.text, etree.HTMLParser())
        names = html.xpath('//dd/div[1]/div[2]/a/div/div[1]/span[1]/text()')
        tags = html.xpath('//dd/div[1]/div[2]/a/div/div[2]/text()')
        releases = html.xpath('//dd/div[1]/div[2]/a/div/div[4]/text()')

        # 删除 空格、换行符、空白字符
        tags = eval(str(tags).replace(' ', '').replace('\\n', ''))
        releases = eval(str(releases).replace(' ', '').replace('\\n', ''))
        for item in tags:
            if len(item) == 0:
                tags.remove(item)
                releases.remove(item)
        
        # 整合成最终结果 ( 取前 10 条电影信息 )
        result = [MaoyanmoiveItem(name=names[i], tag=tags[i], release=releases[i]) for i in range(10)]

        return result

