# Generated by Django 3.0.6 on 2020-05-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('USR', 'Пользователь'), ('RED', 'Редактор'), ('ADM', 'Админ')], default='USR', max_length=3),
        ),
    ]