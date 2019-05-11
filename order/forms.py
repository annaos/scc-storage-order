from django.forms import ModelForm
from .models import Order


class OrderSimpleForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['state', 'create_date', 'submitter']
