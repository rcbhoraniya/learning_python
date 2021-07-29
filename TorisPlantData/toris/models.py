from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import *

# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return str(self.name)


class Operator(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    product_code = models.IntegerField(primary_key=True)
    color_marking_on_bobin = models.CharField(max_length=200)
    tape_color = models.CharField(max_length=100)
    req_denier = models.CharField(max_length=10)
    req_gramage = models.DecimalField(max_digits=10, decimal_places=2)
    req_tape_width = models.DecimalField(max_digits=10, decimal_places=2)
    cutter_spacing = models.DecimalField(max_digits=10, decimal_places=2)
    stock_of_bobin = models.DecimalField(max_digits=10, decimal_places=2)
    req_streanth_per_tape_in_kg = models.DecimalField(max_digits=10, decimal_places=2)
    req_elongation_percent = models.DecimalField(max_digits=10, decimal_places=2)
    streanth = models.DecimalField(max_digits=10, decimal_places=2)
    tanacity = models.DecimalField(max_digits=10, decimal_places=2)
    pp_percent = models.DecimalField(max_digits=10, decimal_places=2)
    filler_percent = models.DecimalField(max_digits=10, decimal_places=2)
    shiner_percent = models.DecimalField(max_digits=10, decimal_places=2)
    color_percent = models.DecimalField(max_digits=10, decimal_places=2)
    tpt_percent = models.DecimalField(max_digits=10, decimal_places=2)
    uv_percent = models.DecimalField(max_digits=10, decimal_places=2)
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.product_code)
    def get_absolute_url(self):
        return reverse('toris:product_detail', args=[self.pk])


class PlantProduction(models.Model):
    SHIFT_CHOICES = (("Day", "DAY"), ("Night", "NIGHT"))
    PLANT_CHOICES = (("TPF", "TPF"), ("TPP", "TPP"))
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)
    date = models.DateField('date production')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='DAY')
    operator_name = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True)
    no_of_winderman = models.IntegerField()
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    end_reading = models.IntegerField()
    start_reading = models.IntegerField()
    wastage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.product_code)

    def get_absolute_url(self):
        return reverse('toris:production_detail', args=[self.pk])

    objects = models.Manager()
    plant_production = PlantProductionManager()

class Order(models.Model):
    order_date = models.DateField('date order')
    customer_name = models.CharField(max_length=200)
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_qty = models.IntegerField()

    def __str__(self):
        return str(self.customer_name)
    def get_absolute_url(self):
        return reverse('toris:order_detail', args=[self.pk])