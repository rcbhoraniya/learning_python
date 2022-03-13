from django.db import models
from .models import *


# class PlantProductionManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().order_by('date','plant')
class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        # return super().get_queryset().filter(is_deleted=False)
        return super().get_queryset().filter(deleted_at__isnull=True)


# class PlantQuerySet(models.QuerySet):
#     def tpf_day(self):
#         return self.filter(plant__name='TPF', shift='Day')
#
#     def tpf_night(self):
#         return self.filter(plant__name='TPF', shift='Night')
#
#     def tpp_day(self):
#         return self.filter(plant__name='TPP', shift='Day')
#
#     def tpp_night(self):
#         return self.filter(plant__name='TPP', shift='Night')


