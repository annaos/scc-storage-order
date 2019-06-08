from django.db import models
from django.utils import timezone


class Person(models.Model):
    username = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    institute = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50)
