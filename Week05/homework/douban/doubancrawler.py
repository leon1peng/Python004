import requests
from lxml import etree
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework.settings')
django.setup()
from .models import Movie


def dou_ban_movie():
    url = "https://movie.douban.com/subject/26794435/comments?start={}&limit=20&status=P&sort=new_score"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.100 Safari/537.36",
        "Referer": "https://movie.douban.com/subject/26794435/",
    }
    for i in range(5):
        url = url.format(str(20*i))
        response = requests.get(url=url, headers=headers)
        html = etree.HTML(response.text, etree.HTMLParser())
        stars = html.xpath('//*[@id="comments"]/div//div[2]/h3/span[2]/span[2]/@class')
        print(stars)
        comments = html.xpath('//*[@id="comments"]/div//div[2]/p/span/text()')
        for n in range(len(stars)):
            star = int(stars[i].replace("allstar", "").replace("0 rating", ""))
            Movie.objects.create(name="哪吒之魔童降世", star=star, comment=comments[i])


if __name__ == '__main__':
    dou_ban_movie()
