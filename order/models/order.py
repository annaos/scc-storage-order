from django.db import models
from django.utils import timezone
from .person import Person


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
    abstract = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    directory_name = models.CharField(max_length=50)
    protocol_ssh = models.BooleanField(verbose_name='SSH', default=True)
    protocol_sftp = models.BooleanField(verbose_name='SFTP', default=True)
    protocol_scp = models.BooleanField(default=True)
    protocol_cifs = models.BooleanField()
    protocol_nfs = models.BooleanField()
    nfs_network = models.CharField(max_length=50, null=True, blank=True)
    owner_name = models.CharField(max_length=50)
    group_name = models.CharField(max_length=50)
    group_permission = models.CharField(
        max_length=50,
        choices=PERMISSION_CHOICES,
        default=PERMISSION_NONE,
    )
    group_cifsacls = models.BooleanField()

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

    def __str__(self):
        return self.project_name

    def is_new(self):
        return self.state == self.NEW

    def is_pending(self):
        return self.state == self.PENDING

    def is_approved(self):
        return self.state == self.APPROVED

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
