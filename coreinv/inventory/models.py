from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .managers import *
from django.utils import timezone
import datetime

now = datetime.datetime.now()


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
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

# inventory models

class Product(SoftDeleteModel):
    UNIT_CHOICE = [('Kg', 'Kg'), ('Litter', 'Litter'), ('Meter', 'Meter'),('Pkt','Packet'),('Nos','Nos')]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, unique=True)
    hsn = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICE)
    rate_without_gst = models.DecimalField(max_digits=10, decimal_places=2 )
    profit_margin_percentage = models.DecimalField(max_digits=10, decimal_places=2 )
    gst_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

    def purchase_price_with_gst(self):
        return self.rate_without_gst * self.gst_percentage / 100 + self.rate_without_gst

    def salse_price_with_gst(self):
        return self.purchase_price_with_gst() * self.profit_margin_percentage / 100 + self.purchase_price_with_gst()

    def salse_price_without_gst(self):
        return self.salse_price_with_gst() * 100 / (100 + self.gst_percentage)

    def get_absolute_url(self):
        return reverse('inventory:new-inventory')

class Inventory(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    current_stock = models.IntegerField(default=0)
    alert_level = models.IntegerField(default=0)

    class Meta:
        ordering = ('product',)

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse('inventory:product-list')


# class State(SoftDeleteModel):
#     state_name = models.CharField(max_length=200, blank=True, null=True,unique=True)
#
#     class Meta:
#         ordering = ('state_name',)
#
#     def __str__(self):
#         return self.state_name
#
#
# class District(SoftDeleteModel):
#     district_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
#     district_name = models.CharField(max_length=200, blank=True, null=True)
#
#     class Meta:
#         ordering = ('district_name',)
#
#     def __str__(self):
#         return self.district_name


class UserProfile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_title = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(max_length=400, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    business_gstin = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

