from django.db import models
from django.utils import timezone


class Person(models.Model):
    username = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    institute = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50)
    admin = models.BooleanField(null=True)

    orders = models.ManyToManyField(
        'order.Order',
        through='PersonOrder',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    def __str__(self):
        return self.firstname
