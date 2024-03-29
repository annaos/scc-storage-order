# Generated by Django 2.2.1 on 2019-08-12 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20190810_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='abstract',
            field=models.TextField(blank=True, help_text='Please describe the scientific objectives of your project', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='capacity',
            field=models.PositiveIntegerField(help_text='Expected storage capacity in TB (1 TB = 1000 GB)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='directory_name',
            field=models.CharField(help_text='What should be the name of the project directory? We recommend using a short project acronmy. Allowed characters are "a-z 0-9 _ -"', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_date',
            field=models.DateField(help_text='End of the project'),
        ),
        migrations.AlterField(
            model_name='order',
            name='group_name',
            field=models.CharField(help_text="Which group should get access to your project directory (e.g. OE-ProjectName-LSDF)? Please, leave this field empty if you don't want to share your data or contact your ITB to create a group", max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, help_text='Please describe your technical requirements', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner_name',
            field=models.CharField(help_text='Who should be the owner the project directory? The owner can be a KIT user (e.g. ab1234) or a KIT service account (e.g. OE-ProjectName-0001). Please, contact your ITB to create a service account.', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='protocol_nfs',
            field=models.BooleanField(help_text='Has to be one or many IPs or Subnets (for example 141.52.000.0/24)', verbose_name='NFS V3 (Client needs to be connected to KIT-IDM)'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='order.Order')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
