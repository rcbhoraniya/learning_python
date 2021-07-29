from django.contrib import admin

# Register your models here.
from .models import Stock,Stock_price

admin.site.register(Stock)
admin.site.register(Stock_price)