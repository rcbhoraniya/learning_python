from django.db import models
from .models import *


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        # return super().get_queryset().filter(is_deleted=False)
        return super(SoftDeleteManager, self).get_queryset().filter(deleted_at__isnull=True)


