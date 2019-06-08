from django.forms import ModelForm
from .models.order import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import models


class OrderSimpleForm(ModelForm):
    headPerson = models.CharField(max_length=100) #TODO check if it work

    class Meta:
        model = Order
        exclude = ['state', 'create_date', 'submitter']
        help_texts = {
            'abstract': 'Describe your project.',
        }


class EditOrderForm(OrderSimpleForm):
    def __init__(self, *args, **kwargs):
        super(EditOrderForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].disabled = True
