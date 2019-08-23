from django.db import models
from django.utils import timezone
from .person import Person
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    NEW = 'NEW'
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    STATE_CHOICES = (
        (NEW, 'new'),
        (PENDING, 'pending'),
        (APPROVED, 'approved'),
    )

    PERMISSION_NONE = 'none'
    PERMISSION_READ = 'read'
    PERMISSION_READ_WRITE = 'read and write'
    PERMISSION_CHOICES = (
        (PERMISSION_NONE, 'No permissions'),
        (PERMISSION_READ, 'Read Only'),
        (PERMISSION_READ_WRITE, 'Read/Write'),
    )

    project_name = models.CharField(max_length=150)
    abstract = models.TextField(null=True, blank=True, help_text=_('Please describe the scientific objectives of your project'))
    notes = models.TextField(null=True, blank=True, help_text=_('Please describe your technical requirements'))
    end_date = models.DateField()
    capacity = models.PositiveIntegerField(help_text=_('Expected storage capacity in TB (1 TB = 1000 GB)'))
    directory_name = models.CharField(max_length=50, help_text=_('What should be the name of the project directory? We recommend using a short project acronmy. Allowed characters are "a-z 0-9 _ -"'))
    protocol_cifs = models.BooleanField(verbose_name=_('CIFS'))
    protocol_nfs = models.BooleanField(verbose_name=_('NFS V3 (Client needs to be connected to KIT-IDM)'))
    nfs_network = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('NFS Client networks*'), help_text=_('Has to be one or many IPs or Subnets (for example 141.52.000.0/24)'))
    owner_name = models.CharField(max_length=50, help_text=_('Who should be the owner the project directory? The owner can be a KIT user (e.g. ab1234) or a KIT service account (e.g. OE-ProjectName-0001). Please, contact your ITB to create a service account.'))
    group_name = models.CharField(max_length=50, help_text=_('Which group should get access to your project directory (e.g. OE-ProjectName-LSDF)? Please contact your ITB to create a group.'))
    group_permission = models.CharField(
        max_length=50,
        choices=PERMISSION_CHOICES,
        default=PERMISSION_NONE,
    )
    group_cifsacls = models.BooleanField(verbose_name=_('Extended group permissions (ACLs)'))

    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True)
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=NEW,
    )
    persons = models.ManyToManyField(
        Person,
        through='PersonOrder',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_date = timezone.now()

    def save(self, *args, **kwargs):
        self.modify_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_name

    def is_new(self):
        return self.state == self.NEW

    def is_pending(self):
        return self.state == self.PENDING

    def is_approved(self):
        return self.state == self.APPROVED

    def alert_color(self):
        if self.is_approved():
            return 'success'
        if self.is_pending():
            return 'warning'
        if self.is_new():
            return 'dark'
        return 'light'

    def owner(self):
        from .personorder import PersonOrder
        return self.__get_person(PersonOrder.ROLE_OWNER)

    def head(self):
        from .personorder import PersonOrder
        return self.__get_person(PersonOrder.ROLE_HEAD)

    def tech(self):
        from .personorder import PersonOrder
        return self.__get_person(PersonOrder.ROLE_TECH)

    def __get_person(self, role):
        from .personorder import PersonOrder
        #TODO if you want more persons with same role, make here tuple
        person_order = PersonOrder.objects.filter(order=self).filter(role=role).first()
        if person_order is None:
            return None
        return person_order.person

    def has_person(self, person):
        from .personorder import PersonOrder
        person_order = PersonOrder.objects.filter(order=self).filter(person=person).first()
        if person_order is None:
            return False
        return True

    def next_state(self):
        if self.state == Order.NEW:
            return Order.PENDING
        if self.state == Order.PENDING:
            return Order.APPROVED
        return None
