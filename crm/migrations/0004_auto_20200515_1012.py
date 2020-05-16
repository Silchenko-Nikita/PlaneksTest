# Generated by Django 3.0.6 on 2020-05-15 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20200515_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_status',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')], default=1),
        ),
    ]