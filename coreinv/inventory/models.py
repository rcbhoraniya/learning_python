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


class Product(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    UNIT_CHOICE = [('Kg', 'Kg'), ('Litter', 'Litter'), ('Meter', 'Meter')]
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

    def get_absolute_url(self):
        return reverse('inventory:new-stock')

class Stock(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
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


# contains suppliers
class Supplier(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    # state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    # district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    gstin = models.CharField(max_length=15, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Customer(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    # customer_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    # customer_district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=14)
    email = models.EmailField(blank=True, null=True, max_length=100)
    gstin = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


# contains the purchase bills made

class PurchaseInvoice(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_number = models.CharField(max_length=20)
    date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    invoice_json = models.TextField()
    total_amt_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_cgst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_sgst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_igst = models.DecimalField(max_digits=10, decimal_places=2)
    igstcheck = models.BooleanField()
    eway_number = models.CharField(max_length=20, blank=True, null=True)
    lr_number = models.CharField(max_length=10, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    po_number = models.CharField(max_length=50, blank=True, null=True)
    challan_number = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
            ordering = ('date',)

    def __str__(self):
        return "Bill no: " + str(self.invoice_number)

    def get_items_list(self):
        return PurchaseInvoiceItem.objects.filter(purchaseinvoice=self)

    def get_total_price(self):
        purchaseitems = PurchaseInvoiceItem.objects.filter(purchaseinvoice=self)
        total = 0
        for item in purchaseitems:
            total += item.amt_with_gst
        return total


class PurchaseInvoiceItem(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    purchaseinvoice = models.ForeignKey(PurchaseInvoice, on_delete=models.SET_NULL, null=True,
                                       related_name='purchaseinvoiceitem')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    rate_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_cgst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_sgst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_igst = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('purchaseinvoice',)

    def __str__(self):
        return  str(self.purchaseinvoice) + ", Product = " + self.product.name


class Invoice(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_number = models.IntegerField()
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    invoice_json = models.TextField()
    total_amt_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_without_gst=models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_cgst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_sgst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt_igst = models.DecimalField(max_digits=10, decimal_places=2)
    igstcheck = models.BooleanField()
    eway_number = models.CharField(max_length=20, blank=True, null=True)
    lr_number = models.CharField(max_length=10, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    po_number = models.CharField(max_length=50, blank=True, null=True)
    challan_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ('invoice_number',)

    def __str__(self):
        return "Bill no: " + str(self.invoice_number)

    def get_items_list(self):
        return InvoiceItem.objects.filter(invoice=self)

    def get_total_price(self):
        saleitems = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in saleitems:
            total += item.amt_with_gst
        return total

    def get_total_gst(self):
        if self.igstcheck == True:
            gst = self.total_amt_igst
        else:
            gst = self.total_amt_cgst + self.total_amt_sgst
        return gst


class InvoiceItem(SoftDeleteModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name='invoiceitem')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    rate_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_with_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_without_gst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_cgst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_sgst = models.DecimalField(max_digits=10, decimal_places=2)
    amt_igst = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('invoice',)

    def __str__(self):
        return str(self.invoice) + ", Product = " + self.product.name
