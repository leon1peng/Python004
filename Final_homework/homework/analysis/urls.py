from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"index", views.index),
    url(r"category", views.category_insert),
    url(r"computer-game/", views.commodity),
    url(r"soda/", views.commodity),
    url(r"smart-phone/", views.commodity),
    url(r"shampoo/", views.commodity),
    url(r"search/keyword/", views.search_keyword),
    url(r"search/datetime/", views.search_datetime),

    # url(r"", views.index),
    # url(r"avg", views.avg_sentiment_and_score),
]
