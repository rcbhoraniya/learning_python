from .managers import *
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

now = datetime.now


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


# ========================== Saas Data models ==================================
class State(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Districts(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class BussinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=400, blank=True, null=True)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(Districts, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gst = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.title


# ======================= Invoice Data models =================================

class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=250, blank=True, null=True)
    customer_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    customer_district = models.ForeignKey(Districts, null=True, blank=True, on_delete=models.SET_NULL)
    customer_city = models.CharField(max_length=50, blank=True, null=True)
    customer_zip = models.CharField(max_length=10, blank=True, null=True)
    customer_phone = models.CharField(max_length=14, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_gst = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.customer_name


class Vendor(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    vendor_name = models.CharField(max_length=200)
    vendor_address = models.CharField(max_length=250, blank=True, null=True)
    vendor_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    vendor_district = models.ForeignKey(Districts, null=True, blank=True, on_delete=models.SET_NULL)
    vendor_city = models.CharField(max_length=50, blank=True, null=True)
    vendor_zip = models.CharField(max_length=10, blank=True, null=True)
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=200)
    vendor_email = models.EmailField(blank=True, null=True)
    vendor_gst = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.vendor_name

class Product(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=200)
    product_hsn = models.CharField(max_length=50, null=True, blank=True)
    product_unit = models.CharField(max_length=50)
    product_gst_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    product_record_level = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.product_name)


class Purchase(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    number = models.IntegerField()
    date = models.DateField()
    purchase_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='invoices')
    product = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.number) + " | " + str(self.date)


class Invoice(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    number = models.IntegerField()
    date = models.DateField()
    sales_quantity = models.PositiveIntegerField()
    sales_price_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='invoices')
    product = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.number) + " | " + str(self.date)
