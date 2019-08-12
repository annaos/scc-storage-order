from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    institute = models.CharField(max_length=100, null=True, blank=True)

    orders = models.ManyToManyField(
        'order.Order',
        through='PersonOrder',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    def __str__(self):
        return self.first_name
