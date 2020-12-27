"""
Author: Leon.Peng
Create DateTime: 12-24-2020 21:23
Comment: No comment

running this crawler
1. cd CommodityScrapy
2. scrapy crawl soda
"""
import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from django.db.models import Avg
from lxml import etree
import re
import datetime
from ..items import CommodityItem, CommentItem
from ..sentiment_analysis.comments_analysis import sentiment_analysis
# noinspection PyUnresolvedReferences
from analysis.models import Commodity, Comments, Category


class SodaSpider(scrapy.Spider):
    name = 'soda'
    allowed_domains = ['smzdm.com']
    start_urls = ['http://smzdm.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment_map = dict()
        self.commodities = ["qipaoshui", "zhinengshouji", "diannaoyouxi", "xifahufa"]
        self.commodity_number = []

    def start_requests(self):
        # 实际运行时用的代码
        for keyword in self.commodities:
            soda_url = "https://www.smzdm.com/fenlei/" + keyword + "/h1c1s0f0t0p1/#feed-main/"
            yield Request(soda_url, callback=self.parse)

        # 测试时用的代码
        # soda_url = "https://www.smzdm.com/fenlei/qipaoshui/h1c1s0f0t0p1/#feed-main/"
        # yield Request(soda_url, callback=self.parse)

    def parse(self, response, **kwargs):
        html = etree.HTML(response.text, etree.HTMLParser())
        # 必要数据： 商品详情界面链接 （包含商品编号信息在链接中）
        detail_links = html.xpath('//*[@id="feed-main-list"]/li//div/div[2]/h5/a/@href')
        print(f"Link: {len(detail_links)} {detail_links}")
        # 必要数据： 商品名
        titles = html.xpath('//*[@id="feed-main-list"]/li//div/div[2]/h5/a/text()')
        titles = [re.sub(".*?: | [0-9]{3}.*?[罐瓶]| \\*.件| \\+凑单品", "", title) for title in titles]
        # 必要数据： 商品的评论总数 和 评论界面的连接
        comment_xpath = '//*[@id="feed-main-list"]/li//div/div[2]/div[@class="z-feed-foot"]/div[1]/a[2]'
        comments_link = html.xpath(comment_xpath + '/@href')
        comments_count = [int(num) for num in html.xpath(comment_xpath + '/span/text()')]
        # 非必要数据： 商品价格
        prices = [price.replace(" ", "").replace("\n", "") for price in
                  html.xpath('//*[@id="feed-main-list"]/li//div/div[2]/div[1]/a/text()')]
        prices = list(filter(lambda s: s and s.strip(), prices))
        # 非必要数据： 商品上架时间
        s_xpath = '//*[@id="feed-main-list"]/li//div/div[2]/div/div[2]/span'
        on_sales = [item.replace(" ", "").replace("\n", "").replace("\t", "") for item in
                    html.xpath(s_xpath + '/text()')]
        on_sales = list(filter(lambda s: s and s.strip(), on_sales))
        # 非必要数据： 商品来源
        sources = [source.replace(" ", "").replace("\n", "") for source in html.xpath(s_xpath + '/a/text()')]

        if len(titles) == len(comments_link) == len(comments_count):
            # 获取排名第十的商品的评论数 top_10
            top_10 = sorted(comments_count)[-10] if len(comments_count) > 10 else min(comments_count)

            for i in range(len(comments_count)):
                # 爬取排名前十的商品和评论，若要爬取界面全部商品，注释下面这行代码，调节代码格式即可
                if comments_count[i] >= top_10:
                    category = re.sub("https:.*lei/|/h1c1s0f0t0p1.*", "", response.url)
                    com_num = re.sub("https:.*/p/|/", "", detail_links[i])
                    self.commodity_number.append(com_num)
                    check_obj = Commodity.objects.filter(com_num=com_num).first()
                    if not check_obj:
                        # 保存商品界面的数据
                        category_obj = Category.objects.filter(name=category).first()
                        sale_time = self.process_datetime(on_sales[i][:5] + " " + on_sales[i][5:])
                        commodity_item = CommodityItem(com_num=com_num, commodity=titles[i], price=prices[i],
                                                       on_sale=sale_time, avg_sentiment="", avg_score="",
                                                       commodity_from=sources[i], detail_link=detail_links[i],
                                                       comment_count=comments_count[i], comment_link=comments_link[i],
                                                       last_comment="", category_id=category_obj)
                        yield commodity_item
                        num = category_obj.count
                        print(f"Test num: {type(num)} {num}")
                        category_obj.count += 1
                        category_obj.save()

                    # 继续爬取评论页的评论
                    self.comment_map[comments_link[i]] = [titles[i], comments_count[i], 1, category]
                    yield Request(comments_link[i], callback=self.comment_parse)
        else:
            print("Error: 401")
            return

    def comment_parse(self, response):
        # 相同商品的评论界面链接都使用首页链接
        url = re.sub("p[0-9]{1,2}?/", "", response.url + "#comments")
        print(f"Url: {url}")
        # 下面 4 行代码只为数据展示，观察使用，可删除
        show_name = self.comment_map[url][0]
        show_count = self.comment_map[url][1]
        show_category = self.comment_map[url][3]
        print(f"=-=-=-=-= {show_name} {show_count} {show_category} =-=-=-=-=")

        # 爬虫界面解析
        page = re.sub("<img .*?>|<br>", "", response.text)
        html = etree.HTML(page, etree.HTMLParser())
        # 必要数据 (核心数据): 评论
        comment_xpath1 = '//div[@id="commentTabBlockNew"]/ul/li//div[2]/div[2]/div[1]/p/span/text()'
        comment_xpath2 = '//div[@id="commentTabBlockNew"]/ul[1]/li//div[2]/div[3]/div[1]/p/span/text()'
        comments = [comment.replace(" ", "") for comment in html.xpath(comment_xpath1 + '|' + comment_xpath2)]
        # 非必要数据： 用户
        xpath_user = '//div[@id="commentTabBlockNew"]/ul[1]/li/div[2]/div[1]'
        usernames = html.xpath(xpath_user + '/a/span[@itemprop="author"]/text()')
        # 非必要数据： 评论发起时间
        comments_time = html.xpath(xpath_user + '/div[1]/text()')

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # =-= 1. 获取该商品在 Commodity 表中的信息 （获取到该 ORM 对象即可：作用 -> 赋值给外键） 
        # =-= 2. 更新最新一条评论的时间到 Commodity 表中
        # =-= 3. last_data_time: 该变量保存该商品 Commodity 表中最新评论的时间 -> 用来判断是否终止爬虫
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # com_num 是商品编号，在 url 中可以获取到该信息： 用来获取 Commodity ORM 对象
        com_num = re.sub("https:.*?/p/", "", response.url)[:8]
        commodity_obj = Commodity.objects.filter(com_num=com_num).first()  # 该查询一定有结果
        # 正则匹配爬虫链接，匹配失败为首页。因为首页第一条为最新评论
        last_comment = re.search("p[0-9]{1,2}?/", response.url)
        if not last_comment:  # 首页
            # 比较 Commodity 表中最新评论时间 和 首页第一条评论时间，判断是否需要更新
            last_page_time = self.process_datetime(comments_time[0])
            if commodity_obj.last_comment:
                last_data_time = datetime.datetime.strptime(commodity_obj.last_comment, "%Y-%m-%d %H:%M:%S")
                if last_data_time == last_page_time:  # 若数据库最新时间和首页第一条时间相同，停止爬取评论
                    return
                # 更新 Connodity 表中最新评论时间
                commodity_obj.last_comment = datetime.datetime.strftime(last_page_time, "%Y-%m-%d %H:%M")
                commodity_obj.save()
            else:
                last_data_time = None
        else:
            last_data_time = response.meta["init_from_leon"]

        # 保存数据到数据库
        for i in range(len(comments)):
            # 判断该数据是否存在 Comments 表中： 存在 -> 终止爬虫; 不存在 -> 保存数据
            comment_time = self.process_datetime(comments_time[i])
            check_obj = Comments.objects.filter(author=usernames[i], comment=comments[i], comment_time=comment_time).first()
            if check_obj:
                return
            else:
                # 核心结果: 将评论做情感分析，得到结果，并保存
                sentiment_score = sentiment_analysis(comments[i])
                sentiment = "正面" if sentiment_score >= 0.5 else "负面"
                category_obj = Category.objects.filter(name=show_category).first()
                comment_item = CommentItem(author=usernames[i], comment=comments[i], sentiment=sentiment,
                                           sentiment_score=sentiment_score, comment_time=comment_time,
                                           commodity_id=commodity_obj, category_id=category_obj)
                yield comment_item

        # 判断是否爬取下一页评论： 递归该方法
        if len(comments) >= 30:
            self.comment_map[url][2] += 1
            page_num = str(self.comment_map[url][2])
            next_url = url.replace("#comments", "") + "p" + page_num + "#comments"
            yield Request(next_url, callback=self.comment_parse, meta={"init_from_leon": last_data_time})
    
    @staticmethod
    def process_datetime(str_datetime: str):
        """
        将 string 类型的时间 转化为 datetime 类型
        """
        print(f"String datetime: {str_datetime}")
        today = datetime.datetime.now()
        year = today.year
        if "小时前" in str_datetime:  # 14小时前
            comment_time = today - datetime.timedelta(hours=int(str_datetime.replace("小时前", "")))
        elif "-" in str_datetime:  # 12-24 13:24
            comment_time = datetime.datetime.strptime(str(year) + "-" + str_datetime, "%Y-%m-%d %H:%M")
        elif "分钟前" in str_datetime:  # 42分钟前
            comment_time = today - datetime.timedelta(minutes=int(str_datetime.replace("分钟前", "")))
        else:
            error_time = datetime.datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            print(type(error_time - error_time), error_time - error_time)
            return -1
        print(f"Comment datetime: {comment_time}")
        return comment_time

    def __del__(self):
        for num in self.commodity_number:
            commodity_obj = Commodity.objects.filter(com_num=num).first()
            avg_score = Comments.objects.filter(commodity_id=commodity_obj.id).all().aggregate(Avg('sentiment_score'))
            avg_score = avg_score['sentiment_score__avg']
            if avg_score is None:
                commodity_obj.avg_sentiment = ''
                commodity_obj.avg_score = ''
            else:
                avg_sentiment = "正面" if avg_score >= 0.5 else "负面"
                commodity_obj.avg_sentiment = avg_sentiment
                commodity_obj.avg_score = avg_score
            commodity_obj.save()
            commodity_obj.save()
        print(f"爬虫结束！")


def commodity_crawler():
    process = CrawlerProcess()
    process.crawl(SodaSpider)
    process.start()


if __name__ == "__main__":
    SodaSpider.process_datetime("14小时前")
    SodaSpider.process_datetime("12-24 13:24")
    SodaSpider.process_datetime("42分钟前")
    SodaSpider.process_datetime("error")
