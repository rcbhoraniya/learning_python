from django.db import models
from .models import *
# class PlantProductionManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().order_by('date','plant')
class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        # return super().get_queryset().filter(is_deleted=False)
        return super().get_queryset().filter(deleted_at__isnull=True)