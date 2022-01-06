from django.db import models
from . import StatusChoice


class StatusModel(models.Model):
    active_status = models.SmallIntegerField(choices=StatusChoice.CHOICES, default=StatusChoice.ACTIVE, null=False)

    class Meta:
        abstract = True
