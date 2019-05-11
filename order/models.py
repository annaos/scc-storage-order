from django.db import models
from django.utils import timezone


class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    institute = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)


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

    submitter = models.CharField(max_length=50)
    project_name = models.CharField(max_length=150)
    customer1 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='order1')
    customer2 = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='order2', null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    directory_name = models.CharField(max_length=50)
    protocol_ssh = models.BooleanField(verbose_name='SSH')
    protocol_sftp = models.BooleanField(verbose_name='SFTP')
    protocol_scp = models.BooleanField()
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
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=NEW,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_date = timezone.now()
        # TODO what is it??
        self.submitter = ""

    def __str__(self):
        return self.project_name

    def is_new(self):
        return self.state == self.NEW

    def is_pending(self):
        return self.state == self.PENDING

    def is_approved(self):
        return self.state == self.APPROVED
