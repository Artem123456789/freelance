from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    customer_description = models.TextField(null=True, blank=True)
    employee_description = models.TextField(null=True, blank=True)
    employee_rating = models.IntegerField(null=True, blank=True)
    customer_rating = models.IntegerField(null=True, blank=True)
