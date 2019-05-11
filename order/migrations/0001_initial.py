# Generated by Django 2.2.1 on 2019-05-11 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('institute', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitter', models.CharField(max_length=50)),
                ('project_name', models.CharField(max_length=150)),
                ('abstract', models.TextField(null=True)),
                ('notes', models.TextField(null=True)),
                ('end_date', models.DateField()),
                ('capacity', models.PositiveIntegerField()),
                ('directory_name', models.CharField(max_length=50)),
                ('protocol_ssh', models.BooleanField(verbose_name='SSH')),
                ('protocol_sftp', models.BooleanField(verbose_name='SFTP')),
                ('protocol_scp', models.BooleanField()),
                ('protocol_cifs', models.BooleanField()),
                ('protocol_nfs', models.BooleanField()),
                ('nfs_network', models.CharField(max_length=50, null=True)),
                ('owner_name', models.CharField(max_length=50)),
                ('group_name', models.CharField(max_length=50)),
                ('group_permission', models.CharField(choices=[('none', 'No permissions'), ('read', 'Read Only'), ('read and write', 'Read/Write')], default='none', max_length=50)),
                ('group_cifsacls', models.BooleanField()),
                ('create_date', models.DateTimeField()),
                ('state', models.CharField(choices=[('NEW', 'new'), ('PENDING', 'pending'), ('APPROVED', 'approved')], default='NEW', max_length=50)),
                ('customer1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order1', to='order.Person')),
                ('customer2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order2', to='order.Person')),
            ],
        ),
    ]