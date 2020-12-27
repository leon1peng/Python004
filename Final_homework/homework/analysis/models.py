from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    name = models.CharField(max_length=32)
    cn_name = models.CharField(max_length=32)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = "Category"


class Commodity(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    com_num = models.CharField(max_length=8)
    commodity = models.CharField(max_length=128)
    price = models.CharField(max_length=128)
    on_sale = models.DateTimeField()
    avg_sentiment = models.CharField(max_length=16, default=None)
    avg_score = models.CharField(max_length=20, default=None)
    commodity_from = models.CharField(max_length=16)
    detail_link = models.TextField()
    comment_count = models.IntegerField()
    comment_link = models.TextField()
    last_comment = models.CharField(max_length=32, default="")
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "Commodity"


class Comments(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    author = models.CharField(max_length=128)
    comment = models.TextField()
    sentiment = models.CharField(max_length=16)
    sentiment_score = models.CharField(max_length=20)
    comment_time = models.DateTimeField()
    commodity_id = models.ForeignKey("Commodity", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "Comments"
