# 4 期 Python 练营 —— 毕业总结
### 目录
1. [总结](#总结)
2. [使用](#使用)
3. [使用](#使用)

### 总结

    毕业作业综合性很强：
        Django 和 Scrapy 的结合, 完成对某些商品评论的爬取，在进行情感分析，最后将结果返回到前端。
    
    我的作业中，爬取了四个商品的评论：
        1. 数据库表： Category(商品种类表)， Commodity(商品表)， Comments(评论表)
        2. 完成的作业要求：
                Scrapy （自动翻页爬取），能正常保存到数据库，数据清洗，Django 正常运行无乱码，
                做情感分析并将结果保存到数据库，Django 上显示结果,关键字搜索，时间搜索,Celery
        3. 部分截屏一放到根目录中(/homework)
    
    代码持续更新(有时间的时候), 暂定添加功能:
        1. JWT Token 登录验证 
        2. 前端表格分页
        3. 添加图表，将数据用图来可视化
        4. 添加 Celery
        ...


### 使用

1. Git 下载所有文件
2. `cd /homework`
3. `pip install -f requirement.txt`
4. `python manage.py runserver`  # 我将数据存了一份在根目录下的`db.sqlite3`中, 
    运行前检查数据库配置
5. 浏览器先输入 `http://127.0.0.1:8000/category` --- 目的是先给 Category 表录入数据，
    目的是为了方便后期写代码，完成后又不想重写这部分，所以就只能麻烦多做这一步
6. `cd /CommodityScrapy`
7. `scrapy crawl soda`  # 手动启动爬虫, Celery部分因为 django,redis和celery的版本冲突,暂时没完成
8. `http://127.0.0.1:8000/index`  # 爬虫结束后，进入 index 就可以使用了

