from django.db import models
from django.urls import reverse

class Stock(models.Model):
    yahoo_symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    nse_symbol = models.CharField(max_length=50,unique=True)
    # exchange = models.CharField(max_length=10)
    # class Meta:
    #     db_table = 'stock'

    def __str__(self):
        return self.name



class Stock_price(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    prev_close =models.FloatField()
    volume = models.IntegerField()
    delivary_volume = models.IntegerField()

    def __str__(self):
        return self.stock_id