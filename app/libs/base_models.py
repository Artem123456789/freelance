from django.db import models
from django.utils.translation import gettext as _


class NamedModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название"), blank=True, null=True)

    class Meta:
        abstract = True
