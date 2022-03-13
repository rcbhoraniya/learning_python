from django.db import models
from django.contrib import admin
from django.urls import reverse
from .managers import *
from django.utils import timezone
import datetime

now = datetime.datetime.now()


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class MarketCap(SoftDeleteModel):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('stocks:marketcap_detail', kwargs={'pk': self.pk})


class Sector(SoftDeleteModel):
    sector = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.sector)

    def get_absolute_url(self):
        return reverse('stocks:sector_detail', kwargs={'pk': self.pk})


class StockMap(SoftDeleteModel):
    name = models.CharField(max_length=200, unique=True)
    m_cap = models.ForeignKey(MarketCap, on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    nse_symbol = models.CharField(max_length=50, unique=True, null=True)
    moneycontrol_symbol = models.CharField(max_length=50, unique=True, null=True)
    yahoo_symbol = models.CharField(max_length=50, unique=True, null=True)
    scrip_code = models.CharField(max_length=10, unique=True, null=True)
    is_portfolio_stock = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('stocks:stockmap_detail', kwargs={'pk': self.pk})

    def get_holding(self):
        objects=StockData.objects.filter(company=self)
        holding=0
        for item in objects:
            holding+=item.side * item.quantity
        return holding
    def get_avg_purchase_price(self):
        quantity = self.get_holding()
        price_sum = 0
        avg_pur_price = 0
        objects = StockData.objects.filter(company=self)
        if quantity > 0:
            for item in objects:
                price_sum += item.side * item.quantity * item.price
                avg_pur_price = price_sum/quantity
            return avg_pur_price
        else:
            for item in objects:
                price_sum += item.side * item.quantity * item.price

            return price_sum

class StockData(SoftDeleteModel):
    date = models.DateTimeField()
    company = models.ForeignKey(StockMap, on_delete=models.SET_NULL, null=True)
    side = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    trade_num = models.BigIntegerField()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return str(self.company)

    def get_quantity(self):
        return self.side * self.quantity

    def get_total_price(self):
        return self.side * self.quantity * self.price

    def get_absolute_url(self):
        return reverse('stocks:stockdata_detail', kwargs={'pk': self.pk})


class HistoricalData(SoftDeleteModel):
    company = models.ForeignKey(StockMap, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    adj_close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return str(self.company)

    def get_absolute_url(self):
        return reverse('stocks:historicaldata_detail', kwargs={'pk': self.pk})


class NSEHistorical(SoftDeleteModel):
    symbol = models.ForeignKey(StockMap, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    prv_close = models.DecimalField(max_digits=12, decimal_places=2)
    last = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    deliverable_volume = models.BigIntegerField()
    deliverble_per = models.DecimalField(max_digits=12, decimal_places=2)


    class Meta:
        ordering = ('date',)

    def __str__(self):
        return str(self.symbol)

    def get_absolute_url(self):
        return reverse('stocks:nsehistorical_detail', kwargs={'pk': self.pk})


class NSEBhavcopy(SoftDeleteModel):
    symbol = models.OneToOneField(StockMap, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    prv_close = models.DecimalField(max_digits=12, decimal_places=2)
    last = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()
    isin = models.CharField(max_length=14, null=True)
    class Meta:
        ordering = ('date',)

    def __str__(self):
        return str(self.symbol)

    def get_absolute_url(self):
        return reverse('stocks:nsebhavcopy_detail', kwargs={'pk': self.pk})


class NSEData(SoftDeleteModel):
    symbol = models.ForeignKey(StockMap, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    open = models.DecimalField(max_digits=12, decimal_places=2)
    dayhigh = models.DecimalField(max_digits=12, decimal_places=2)
    daylow = models.DecimalField(max_digits=12, decimal_places=2)
    lastprice = models.DecimalField(max_digits=12, decimal_places=2)
    previousclose = models.DecimalField(max_digits=12, decimal_places=2)
    change = models.DecimalField(max_digits=12, decimal_places=2)
    pchange = models.DecimalField(max_digits=12, decimal_places=2)
    yearhigh = models.DecimalField(max_digits=12, decimal_places=2)
    yearlow = models.DecimalField(max_digits=12, decimal_places=2)
    totaltradedvolume = models.IntegerField()
    perchange365d = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    perchange30d = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    dayendclose = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    corporate_action = models.CharField(max_length=100, null=True)
    x_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ('symbol',)

    def __str__(self):
        return str(self.symbol)


