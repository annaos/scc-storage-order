from django.db import models
from django.utils import timezone
from .person import Person
from .order import Order
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    text = models.TextField(verbose_name=_('Your comment'))
    create_date = models.DateTimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='comment')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_date = timezone.now()
