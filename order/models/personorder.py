from django.db import models
from django.utils import timezone
from .order import Order
from .person import Person


class PersonOrder(models.Model):
    ROLE_HEAD = 'ROLE_HEAD'
    ROLE_OWNER = 'ROLE_OWNER'
    ROLE_TECH = 'ROLE_TECH'
    ROLE_CHOICES = (
        (ROLE_OWNER, 'ROLE_OWNER'),
        (ROLE_HEAD, 'ROLE_HEAD'),
        (ROLE_TECH, 'ROLE_TECH'),
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='order')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='person')
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )