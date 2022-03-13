from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import *
from django.utils import timezone
import datetime
from django.db.models import Avg, Max, Min, Sum, Count, F

now = datetime.datetime.now()


class SoftDeleteModel(models.Model):
    # is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        # self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


# Create your models here.
class Plant(SoftDeleteModel):
    name = models.CharField(max_length=3, verbose_name='Plant', unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Country(SoftDeleteModel):
    name = models.CharField(max_length=40, verbose_name='Country')
    un_continental = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class State(SoftDeleteModel):
    name = models.CharField(max_length=40, verbose_name='State')

    def __str__(self):
        return str(self.name)


class District(SoftDeleteModel):
    code = models.CharField(max_length=5, null=True)
    state = models.ForeignKey(State, related_name='district', on_delete=models.SET_NULL, null=True,
                              verbose_name='States')
    name = models.CharField(max_length=40, verbose_name='District_name')
    headquarters = models.CharField(max_length=40, verbose_name='Headquarters')

    def __str__(self):
        return str(self.name)


class Designation(SoftDeleteModel):
    designation = models.CharField(max_length=30, verbose_name='Designation', unique=True)

    class Meta:
        ordering = ['designation']

    def __str__(self):
        return str(self.designation)


def upload_to_folder(instance, filename):
    return 'employee_{instance}/{filename}'.format(instance=instance.pk, filename=filename)


class Employee(SoftDeleteModel):
    name = models.CharField(max_length=100, verbose_name='First Name', null=False)
    mname = models.CharField(max_length=100, verbose_name='Middle Name', null=True)
    lname = models.CharField(max_length=100, verbose_name='Last Name', null=True)
    city = models.CharField(max_length=50, verbose_name='City', null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, )
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True)
    mobile1 = models.CharField(max_length=13, verbose_name='Mobile1', null=True)
    mobile2 = models.CharField(max_length=13, verbose_name='Mobile2', null=True)
    aadhhar_no = models.CharField(max_length=16, verbose_name='Aadhhar', null=True)
    designation = models.ForeignKey(Designation, related_name='designations', on_delete=models.SET_NULL, null=True,
                                    verbose_name='Designation')
    photo_image = models.ImageField(_("Image"), upload_to=upload_to_folder, blank=True, null=True)

    # thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True)
    # slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
    # def get_absolute_url(self):
    #     return f'/{self.slug}'
    #
    # def get_image(self):
    #     if self.image:
    #         return 'http://127.0.0.1:8000/'+self.image.url
    #     return ''
    # def get_thumbnail(self):
    #     if self.thumbnail:
    #         return 'http://127.0.0.1:8000/' + self.thumbnail.url
    #     else:
    #         if self.image:
    #             self.thumbnail=self.make_thumbnail(self.image)
    #             self.save()
    #             return 'http://127.0.0.1:8000/' + self.thumbnail.url
    #         else:
    #             return ''

    # def make_thumbnail(self,image,size=(300,200)):


class Product(SoftDeleteModel):
    product_code = models.IntegerField(verbose_name='Product Code', unique=True)
    color_marking_on_bobin = models.CharField(max_length=200, verbose_name='Color marking on bobin', null=True,
                                              default=None)
    tape_color = models.CharField(max_length=100, verbose_name='Tape Color', null=True, default=None)
    denier = models.IntegerField(verbose_name='Denier', null=True, default=None)
    gramage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gramage', null=True, default=None)
    tape_width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tape Width in mm', null=True,
                                     default=None)
    cutter_spacing = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cutter Spacing in mm',
                                         null=True, default=None)
    stock_of_bobin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Bobin Stock', null=True,
                                         default=None)
    streanth_per_tape_in_kg = models.DecimalField(max_digits=10, decimal_places=2,
                                                  verbose_name='Strength per tape in kg', null=True, default=None)
    elongation_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Elongation %', null=True,
                                             default=None)
    tenacity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tanacity', null=True, default=None)
    pp_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='PP %', null=True, default=None)
    filler_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Filler %', null=True,
                                         default=None)
    shiner_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Shiner %', null=True,
                                         default=None)
    color_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Color %', null=True,
                                        default=None)
    tpt_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='TPT %', null=True, default=None)
    uv_percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='UV %', null=True, default=None)
    color_name = models.CharField(max_length=50, verbose_name='Color name', null=True, default=None)

    class Meta:
        ordering = ['product_code']

    def __str__(self):
        return str(self.product_code)

    def get_absolute_url(self):
        return reverse('toris:product_detail', args=[self.pk])

    def getScientifName(self):
        return str(self.product_code) + ' - ' + str(self.color_marking_on_bobin) + " - " + str(self.tape_color);


class PlantProduction(SoftDeleteModel):
    SHIFT_CHOICES = (("Day", "DAY"), ("Night", "NIGHT"))
    plant = models.ForeignKey(Plant, related_name='plants', on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name='Production Date')
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES, default='DAY', verbose_name='Shift')
    operator_name = models.ForeignKey(Employee, related_name='employee_name', on_delete=models.SET_NULL, null=True,
                                      verbose_name='Employee Name')
    no_of_winderman = models.IntegerField()
    product_code = models.ForeignKey(Product, related_name='plant_productions', on_delete=models.CASCADE,
                                     verbose_name='Product Code')
    end_reading = models.IntegerField(verbose_name='End Reading')
    start_reading = models.IntegerField(verbose_name='Start Reading')
    wastage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Wastage')

    # plantmanager = PlantQuerySet.as_manager()
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.product_code)

    def get_absolute_url(self):
        return reverse('toris:production_detail', args=[self.pk])
    @property
    def production_field(self):
        production = int(self.end_reading) - int(self.start_reading)

        return production

    # production = property(production_field)


class Customer(SoftDeleteModel):
    name = models.CharField(max_length=200, verbose_name='Customer Name')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,)
    city = models.CharField(max_length=50, verbose_name='City', null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True,)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True)
    mobile = models.CharField(max_length=13, verbose_name='Mobile', null=True)
    gst_no = models.CharField(max_length=15, verbose_name='GSTNo', null=True)

    def __str__(self):
        return str(self.name)


class Order(SoftDeleteModel):
    order_date = models.DateField('date order',null=True)
    customer_name = models.ForeignKey(Customer,related_name='customers', verbose_name='Customer Name', on_delete=models.SET_NULL,null=True)
    product_code = models.ForeignKey(Product, related_name='orders', on_delete=models.SET_NULL,null=True,
                                     verbose_name='Product Code')
    order_qty = models.IntegerField(verbose_name='Order Quantity in kg',null=True)
    pi_number = models.CharField(max_length=200, verbose_name='PI Number',null=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return str(self.customer_name)

    def get_absolute_url(self):
        return reverse('toris:order_detail', args=[self.pk])
