from django.forms import ModelForm
from .models.order import Order
from .models.comment import Comment
from .models.personorder import PersonOrder
from .models.person import Person
from django import forms
import re
from django.utils.translation import gettext_lazy as _
from datetime import date
from dateutil.relativedelta import relativedelta

# deprecate
class PersonForm(forms.Form):
    email = forms.EmailField(max_length=100)
    firstname = forms.CharField(max_length=100, required=False)
    lastname = forms.CharField(max_length=100, required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class OrderSimpleForm(ModelForm):
    head_email = forms.EmailField(max_length=100, label='Email')
    head_institute = forms.CharField(max_length=300, required=False, label='Institute')
    head_firstname = forms.CharField(max_length=100, required=True, label='Firstname')
    head_lastname = forms.CharField(max_length=100, required=True, label='Lastname')

    tech_email = forms.EmailField(max_length=100, required=False, label='Email')
    tech_institute = forms.CharField(max_length=300, required=False, label='Institute')
    tech_firstname = forms.CharField(max_length=100, required=False, label='Firstname')
    tech_lastname = forms.CharField(max_length=100, required=False, label='Lastname')

    owner_email = forms.EmailField(max_length=100, label='Email')
    owner_institute = forms.CharField(max_length=300, required=False, label='Institute')
    owner_firstname = forms.CharField(max_length=100, required=False, label='Firstname')
    owner_lastname = forms.CharField(max_length=100, required=False, label='Lastname')

    end_date = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        label=_('End of the project'),
        help_text=_('The latest possible date is in 3 years')
    )

    class Meta:
        model = Order
#        fields = ['project_name', 'abstract', 'notes', 'end_date', 'capacity', 'directory_name', 'protocol_ssh', 'protocol_sftp', 'protocol_cifs', 'protocol_nfs', 'nfs_network',
#                  'owner_name', 'group_name', 'group_permission', 'group_cifsacls', 'headPersonEmail', 'headPersonFirstname', 'headPersonLastname']
        exclude = ['state', 'create_date', 'modify_date', 'persons']

    def __init__(self, owner=None, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            owner_person = kwargs['instance'].owner()
            if owner_person is None:
                owner_person = owner
            if owner_person is not None:
                initial['owner_email'] = owner_person.email
                initial['owner_institute'] = owner_person.institute
                initial['owner_firstname'] = owner_person.first_name
                initial['owner_lastname'] = owner_person.last_name
            head_person = kwargs['instance'].head()
            if head_person is None:
                head_person = owner
            if head_person is not None:
                initial['head_email'] = head_person.email
                initial['head_institute'] = head_person.institute
                initial['head_firstname'] = head_person.first_name
                initial['head_lastname'] = head_person.last_name
            tech_person = kwargs['instance'].tech()
            if tech_person is not None:
                initial['tech_email'] = tech_person.email
                initial['tech_institute'] = tech_person.institute
                initial['tech_firstname'] = tech_person.first_name
                initial['tech_lastname'] = tech_person.last_name
            initial['end_date'] = date.today() + relativedelta(years=+3)
        ModelForm.__init__(self, *args, **kwargs)
        self.fields['owner_email'].disabled = True
        self.fields['owner_institute'].disabled = True
        self.fields['owner_firstname'].disabled = True
        self.fields['owner_lastname'].disabled = True

    def save(self, commit=True):
        order = super(OrderSimpleForm, self).save()
        self._create_person_order(order, PersonOrder.ROLE_OWNER, 'owner')
        self._create_person_order(order, PersonOrder.ROLE_HEAD, 'head')
        self._create_person_order(order, PersonOrder.ROLE_TECH, 'tech')
        return order

    def clean(self):
        cleaned_data = super().clean()
        protocol_nfs = cleaned_data.get("protocol_nfs")
        nfs_network = cleaned_data.get("nfs_network")
        if protocol_nfs and not nfs_network:
            error = forms.ValidationError("Must fill NFS Client networks when choosing NFS V3.")
            self.add_error('nfs_network', error)
            raise error

        if cleaned_data.get("end_date") > date.today() + relativedelta(years=+3):
            self.add_error('end_date', "End date should be less than 3 years in the future")

        if not re.match("^[^\s]+$", cleaned_data.get("group_name")):
            self.add_error('group_name', "Group name should not have spaces")

        if not re.match("^[^\s]+$", cleaned_data.get("owner_name")):
            self.add_error('owner_name', "Owner name should not have spaces")

        if not re.match("^[a-zA-Z0-9_-]+$", cleaned_data.get("directory_name")):
            self.add_error('directory_name', "Allowed characters are \"a-z 0-9 _ -\"")

    def _create_person_order(self, order, role, prefix):
        person_email = self.cleaned_data.get(prefix + '_email')
        if person_email.strip():
            try:
                person = Person.objects.get(username=person_email)
            except Person.DoesNotExist:
                try:
                    person = Person.objects.get(email=person_email)
                except Person.DoesNotExist:
                    person = Person()
                    person.email = person_email
                    person.username = person_email
                    person.set_unusable_password()
            person.first_name = self.cleaned_data.get(prefix + '_firstname')
            person.institute = self.cleaned_data.get(prefix + '_institute')
            person.last_name = self.cleaned_data.get(prefix + '_lastname')
            person.save()
            try:
                PersonOrder.objects.get(person=person, order=order, role=role)
            except PersonOrder.DoesNotExist:
                try:
                    PersonOrder.objects.filter(order=order, role=role).delete()
                finally:
                    PersonOrder.objects.create(person=person, order=order, role=role)


class OrderAdminForm(OrderSimpleForm):
    class Meta:
        model = Order
        exclude = ['create_date', 'modify_date', 'persons']


class OrderEditForm(OrderSimpleForm):
    def __init__(self, *args, **kwargs):
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].disabled = True
        self.fields['abstract'].disabled = True
        self.fields['notes'].disabled = True
        self.fields['end_date'].disabled = True
        self.fields['capacity'].disabled = True
        self.fields['directory_name'].disabled = True
        self.fields['protocol_cifs'].disabled = True
        self.fields['protocol_nfs'].disabled = True
        self.fields['nfs_network'].disabled = True
        self.fields['owner_name'].disabled = True
        self.fields['group_name'].disabled = True
        self.fields['group_permission'].disabled = True
        self.fields['group_cifsacls'].disabled = True