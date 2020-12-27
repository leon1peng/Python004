from django.contrib import admin
from .models import Category, Commodity, Comments

# Register your models here.
admin.site.register(Category)
admin.site.register(Commodity)
admin.site.register(Comments)
