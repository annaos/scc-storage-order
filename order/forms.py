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
    head_email = forms.EmailField(max_length=100, label='Email')
    head_institute = forms.CharField(max_length=300, required=False, label='Institute')
    head_firstname = forms.CharField(max_length=100, required=True, label='Firstname')
    head_lastname = forms.CharField(max_length=100, required=True, label='Lastname')

    tech_email = forms.EmailField(max_length=100, label='Email')
    tech_institute = forms.CharField(max_length=300, required=False, label='Institute')
    tech_firstname = forms.CharField(max_length=100, required=False, label='Firstname')
    tech_lastname = forms.CharField(max_length=100, required=False, label='Lastname')


    class Meta:
        model = Order
#        fields = ['project_name', 'abstract', 'notes', 'end_date', 'capacity', 'directory_name', 'protocol_ssh', 'protocol_sftp', 'protocol_cifs', 'protocol_nfs', 'nfs_network',
#                  'owner_name', 'group_name', 'group_permission', 'group_cifsacls', 'headPersonEmail', 'headPersonFirstname', 'headPersonLastname']
        exclude = ['state', 'create_date', 'modify_date', 'persons']
        help_texts = {
            'abstract': 'Please describe the scientific objectives of your project',
            'notes': 'Please describe your technical requirements',
            'end_date': 'End of the project',
            'capacity': 'Expected storage capacity in TB (1 TB = 1000 GB)',
            'directory_name': 'What should be the name of the project directory? We recommend using a short project acronmy. Allowed characters are "a-z 0-9 _ -"',
            'nfs_network': 'Has to be one or many IPs or Subnets (for example 141.52.000.0/24)',
            'owner_name': 'Who should be the owner the project directory? The owner can be a KIT user (e.g. ab1234) or a KIT service account (e.g. OE-ProjectName-0001). Please, contact your ITB to create a service account.',
            'group_name': 'Which group should get access to your project directory (e.g. OE-ProjectName-LSDF)? Please, leave this field empty if you don\'t want to share your data or contact your ITB to create a group',
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            head_person = kwargs['instance'].head()
            if head_person is not None:
                initial['head_email'] = head_person.email
                initial['tech_institute'] = head_person.institute
                initial['head_firstname'] = head_person.firstname
                initial['head_lastname'] = head_person.lastname
            tech_person = kwargs['instance'].tech()
            if tech_person is not None:
                initial['tech_email'] = tech_person.email
                initial['tech_institute'] = tech_person.institute
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


class OrderEditForm(OrderSimpleForm):
    def __init__(self, *args, **kwargs):
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].disabled = True
        self.fields['abstract'].disabled = True
        self.fields['notes'].disabled = True
        self.fields['end_date'].disabled = True
        self.fields['capacity'].disabled = True
        self.fields['directory_name'].disabled = True
        self.fields['protocol_ssh'].disabled = True
        self.fields['protocol_sftp'].disabled = True
        self.fields['protocol_cifs'].disabled = True
        self.fields['protocol_nfs'].disabled = True
        self.fields['nfs_network'].disabled = True
        self.fields['owner_name'].disabled = True
        self.fields['group_name'].disabled = True
        self.fields['group_permission'].disabled = True
        self.fields['group_cifsacls'].disabled = True