from django.forms import ModelForm
from .models.order import Order
from .models.personorder import PersonOrder
from .models.person import Person
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import models
from django import forms

# deprecate
class PersonForm(forms.Form):
    email = forms.EmailField(max_length=100)
    firstname = forms.CharField(max_length=100, required=False)
    lastname = forms.CharField(max_length=100, required=False)


class OrderSimpleForm(ModelForm):
#    head_person_form_set = PersonForm()
#    tech_person_form_set = PersonForm()
    head_email = forms.EmailField(max_length=100)
    head_firstname = forms.CharField(max_length=100, required=False)
    head_lastname = forms.CharField(max_length=100, required=False)

    tech_email = forms.EmailField(max_length=100)
    tech_firstname = forms.CharField(max_length=100, required=False)
    tech_lastname = forms.CharField(max_length=100, required=False)


    class Meta:
        model = Order
#        fields = ['project_name', 'abstract', 'notes', 'end_date', 'capacity', 'directory_name', 'protocol_ssh', 'protocol_sftp', 'protocol_cifs', 'protocol_nfs', 'nfs_network',
#                  'owner_name', 'group_name', 'group_permission', 'group_cifsacls', 'headPersonEmail', 'headPersonFirstname', 'headPersonLastname']
        exclude = ['state', 'create_date', 'modify_date', 'persons']
        help_texts = {
            'abstract': 'Describe your project.',
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            head_person = kwargs['instance'].head()
            if head_person is not None:
                initial['head_email'] = head_person.email
                initial['head_firstname'] = head_person.firstname
                initial['head_lastname'] = head_person.lastname
            tech_person = kwargs['instance'].tech()
            if tech_person is not None:
                initial['tech_email'] = tech_person.email
                initial['tech_firstname'] = tech_person.firstname
                initial['tech_lastname'] = tech_person.lastname

        ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        order = super(OrderSimpleForm, self).save()
        self._create_person_order(order, PersonOrder.ROLE_HEAD, 'head')
        self._create_person_order(order, PersonOrder.ROLE_TECH, 'tech')
        return order

    def _create_person_order(self, order, role, prefix):
        person_email = self.cleaned_data.get(prefix + '_email')
        try:
            person = Person.objects.get(email=person_email)
            # TODO update firstname lastname for existed person? or show fields only per ajax
        except Person.DoesNotExist:
            person = Person()
            person.email = person_email
            person.firstname = self.cleaned_data.get(prefix + '_firstname')
            person.lastname = self.cleaned_data.get(prefix + '_lastname')
            person.save()
        try:
            PersonOrder.objects.get(person=person, order=order, role=role)
        except PersonOrder.DoesNotExist:
            try:
                PersonOrder.objects.filter(order=order, role=role).delete()
            finally:
                PersonOrder.objects.create(person=person, order=order, role=role)


class EditOrderForm(OrderSimpleForm):
    def __init__(self, *args, **kwargs):
        super(EditOrderForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].disabled = True
