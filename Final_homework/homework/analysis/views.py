from django.shortcuts import render
from django.db.models import Avg, Count, Sum
from django.http.response import HttpResponse
from .models import Comments, Commodity, Category
from datetime import datetime, timedelta

NAME_MAP = {
    "diannaoyouxi": "电脑游戏",
    "qipaoshui": "气泡水",
    "zhinengshouji": "智能手机",
    "xifahufa": "洗发水"
}


# Create your viewsere.
def category_insert(request):
    categories = ["qipaoshui", "zhinengshouji", "diannaoyouxi", "xifahufa"]
    for keyword in categories:
        cn_name = NAME_MAP[keyword]
        Category.objects.create(name=keyword, cn_name=cn_name)
        print(f"{keyword} 成功插入数据库！")
    return HttpResponse("成功插入数据库！")


def avg_sentiment_and_score(request):
    commodity_count = Commodity.objects.all().count()
    print(commodity_count)
    for num in range(1, commodity_count + 1):
        commodity_obj = Commodity.objects.filter(id=num).first()
        avg_score = Comments.objects.filter(commodity_id=num).all().aggregate(Avg('sentiment_score'))
        avg_score = avg_score['sentiment_score__avg']
        print(type(avg_score), avg_score)
        if avg_score is None:
            commodity_obj.avg_sentiment = ''
            commodity_obj.avg_score = ''
        else:
            avg_sentiment = "正面" if avg_score >= 0.5 else "负面"
            commodity_obj.avg_sentiment = avg_sentiment
            commodity_obj.avg_score = avg_score
        commodity_obj.save()
    return HttpResponse("成功！")


def index(request):
    category_obj = Category.objects.all()
    soda = dict()
    computer_game = dict()
    smart_phone = dict()
    shampoo = dict()
    for row in category_obj:
        if row.name == "qipaoshui":
            soda["id"] = row.id
            soda["name"] = NAME_MAP['qipaoshui']
            soda["count"] = row.count
        if row.name == "zhinengshouji":
            smart_phone["id"] = row.id
            smart_phone["name"] = NAME_MAP['zhinengshouji']
            smart_phone["count"] = row.count
        if row.name == "diannaoyouxi":
            computer_game["id"] = row.id
            computer_game["name"] = NAME_MAP['diannaoyouxi']
            computer_game["count"] = row.count
        if row.name == "xifahufa":
            shampoo["id"] = row.id
            shampoo["name"] = NAME_MAP['xifahufa']
            shampoo["count"] = row.count
    commodity_name = "所有商品"
    return render(request, 'index.html', locals())


def commodity(request):
    if request.path == "/computer-game/":
        name = "diannaoyouxi"
        commodity_name = "电脑游戏"
    elif request.path == "/soda/":
        name = "qipaoshui"
        commodity_name = "气泡水"
    elif request.path == "/smart-phone/":
        name = "zhinengshouji"
        commodity_name = "智能手机"
    elif request.path == "/shampoo/":
        name = "xifahufa"
        commodity_name = "洗发水"
    else:
        return render(request, 'result.html', locals())
    category_obj = Category.objects.filter(name=name).first()
    commodity_obj = Commodity.objects.filter(category_id=category_obj.id).all()
    comment_obj = Comments.objects.filter(category_id=category_obj.id).all()
    # 评论数量
    counter = commodity_obj.aggregate(Sum('comment_count'))['comment_count__sum']
    # 情感倾向
    score_avg = f"{comment_obj.aggregate(Avg('sentiment_score'))['sentiment_score__avg']:0.2f}"
    # 情感
    sentiment_avg = "正向" if float(score_avg) >= 0.5 else "负向"
    # 正向数量
    plus = comment_obj.filter(sentiment="正面").values('sentiment').count()
    # 负向数量
    minus = comment_obj.filter(sentiment="负面").values('sentiment').count()
    return render(request, 'result.html', locals())


def search_keyword(request):
    keyword = request.GET.get('keyword')
    commodity_name = keyword
    if not keyword:
        error_msg = '请输入关键词'
        return render(request, 'errors.html', {'error_msg': error_msg})

    comment_obj = Comments.objects.filter(comment__icontains=keyword).all()
    if not comment_obj:
        error_msg = '输入关键词不正确，请重新输入...'
        return render(request, 'errors.html', {'error_msg': error_msg})
    counter = comment_obj.count()
    score_avg = f"{comment_obj.aggregate(Avg('sentiment_score'))['sentiment_score__avg']:0.2f}"
    sentiment_avg = "正向" if float(score_avg) >= 0.5 else "负向"
    plus = comment_obj.filter(sentiment="正面").values('sentiment').count()
    minus = comment_obj.filter(sentiment="负面").values('sentiment').count()
    return render(request, 'result.html', locals())


def search_datetime(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    if not start_time and not end_time:
        error_msg = '日期为空，请输入日期...'
        return render(request, 'errors.html', {'error_msg': error_msg})
    commodity_name = "时间：" + start_time + " ~ " + end_time
    start_time = datetime.strptime(start_time, "%Y-%m-%d") if start_time else None
    end_time = datetime.strptime(end_time, "%Y-%m-%d") if end_time else None
    print(f"start time: {start_time}")
    print(f"start time: {end_time}")
    if start_time and end_time:
        print("test1")
        comment_obj = Comments.objects.filter(comment_time__lte=end_time, comment_time__gte=start_time).all()
    else:
        search_time = start_time if start_time else end_time
        add_one = search_time + timedelta(days=1)
        comment_obj = Comments.objects.filter(comment_time__lte=add_one, comment_time__gte=search_time).all()
    if not comment_obj:
        error_msg = '输入日期不正确，请重新输入...'
        return render(request, 'errors.html', {'error_msg': error_msg})
    counter = comment_obj.count()
    score_avg = f"{comment_obj.aggregate(Avg('sentiment_score'))['sentiment_score__avg']:0.2f}"
    sentiment_avg = "正向" if float(score_avg) >= 0.5 else "负向"
    plus = comment_obj.filter(sentiment="正面").values('sentiment').count()
    minus = comment_obj.filter(sentiment="负面").values('sentiment').count()
    return render(request, 'result.html', locals())
