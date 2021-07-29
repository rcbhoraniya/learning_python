from django.db import models
from .models import *
class PlantProductionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('date','plant')