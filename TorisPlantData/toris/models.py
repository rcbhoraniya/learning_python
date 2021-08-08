from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import *
from django.utils import timezone
import datetime
from django.db.models import Avg, Max, Min, Sum, Count, F

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


# Create your models here.
class Plant(SoftDeleteModel):
    name = models.CharField(max_length=3, verbose_name='Plant')

    def __str__(self):
        return str(self.name)


class Operator(SoftDeleteModel):
    name = models.CharField(max_length=200, verbose_name='Operator Name')

    def __str__(self):
        return str(self.name)


class Product(SoftDeleteModel):
    product_code = models.IntegerField(verbose_name='Product Code')
    color_marking_on_bobin = models.CharField(max_length=200, verbose_name='Color marking on bobin')
    tape_color = models.CharField(max_length=100, verbose_name='Tape Color')
    denier = models.IntegerField(verbose_name='Denier')
    gramage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gramage')
    tape_width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tape Width in mm')
    cutter_spacing = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cutter Spacing in mm')
    stock_of_bobin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Bobin Stock')
    streanth_per_tape_in_kg = models.DecimalField(max_digits=10, decimal_places=2,
                                                  verbose_name='Strength per tape in kg')
    elongation_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Elongation %')
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

    def getScientifName(self):
        return str(self.product_code)+' - '+str(self.color_marking_on_bobin) + " - " + str(self.tape_color);


class PlantProduction(SoftDeleteModel):

    SHIFT_CHOICES = (("Day", "DAY"), ("Night", "NIGHT"))
    PLANT_CHOICES = (("TPF", "TPF"), ("TPP", "TPP"))
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)
    # plant = models.CharField(max_length=3, choices=PLANT_CHOICES)
    date = models.DateField(verbose_name='Production Date')
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES, default='DAY', verbose_name='Shift')
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


    def production_field(self ):
        production = self.end_reading - self.start_reading

        return production


class Order(SoftDeleteModel):

    order_date = models.DateField('date order')
    customer_name = models.CharField(max_length=200, verbose_name='Customer Name')
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product Code')
    order_qty = models.IntegerField(verbose_name='Order Quantity in kg')
    pi_number = models.CharField(max_length=200, verbose_name='PI Number')

    def __str__(self):
        return str(self.customer_name)

    def get_absolute_url(self):
        return reverse('toris:order_detail', args=[self.pk])
