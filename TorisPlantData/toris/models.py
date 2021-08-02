from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import *


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=3, verbose_name='Plant')

    def __str__(self):
        return str(self.name)


class Operator(models.Model):
    name = models.CharField(max_length=200, verbose_name='Operator Name')

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    product_code = models.IntegerField(verbose_name='Product Code')
    color_marking_on_bobin = models.CharField(max_length=200, verbose_name='Color marking on bobin')
    tape_color = models.CharField(max_length=100, verbose_name='Tape Color')
    req_denier = models.CharField(max_length=10, verbose_name='Denier')
    req_gramage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gramage')
    req_tape_width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tape Width in mm')
    cutter_spacing = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cutter Spacing in mm')
    stock_of_bobin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Bobin Stock')
    req_streanth_per_tape_in_kg = models.DecimalField(max_digits=10, decimal_places=2,
                                                      verbose_name='Strength per tape in kg')
    req_elongation_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Elongation %')
    streanth = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Strength')
    tanacity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tanacity')
    pp_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='PP %')
    filler_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Filler %')
    shiner_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Shiner %')
    color_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Color %')
    tpt_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='TPT %')
    uv_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='UV %')
    color_name = models.CharField(max_length=50, verbose_name='Color name')

    def __str__(self):
        return str(self.product_code)

    def get_absolute_url(self):
        return reverse('toris:product_detail', args=[self.pk])


class PlantProduction(models.Model):
    SHIFT_CHOICES = (("Day", "DAY"), ("Night", "NIGHT"))
    PLANT_CHOICES = (("TPF", "TPF"), ("TPP", "TPP"))
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)
    # plant = models.CharField(max_length=3, choices=PLANT_CHOICES)
    date = models.DateField(verbose_name='Production Date')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='DAY', verbose_name='Shift')
    operator_name = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True, verbose_name='Operator Name')
    no_of_winderman = models.IntegerField()
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product Code')
    end_reading = models.IntegerField(verbose_name='End Reading')
    start_reading = models.IntegerField(verbose_name='Start Reading')
    wastage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Wastage')

    def __str__(self):
        return str(self.product_code)

    def get_absolute_url(self):
        return reverse('toris:production_detail', args=[self.pk])

    objects = models.Manager()
    plant_production = PlantProductionManager()


class Order(models.Model):
    order_date = models.DateField('date order')
    customer_name = models.CharField(max_length=200, verbose_name='Customer Name')
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product Code')
    order_qty = models.IntegerField(verbose_name='Order Quantity in kg')

    def __str__(self):
        return str(self.customer_name)

    def get_absolute_url(self):
        return reverse('toris:order_detail', args=[self.pk])
