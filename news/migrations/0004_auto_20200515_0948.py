# Generated by Django 3.0.6 on 2020-05-15 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200515_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_status',
            field=models.CharField(choices=[('IA', 'Неактивна'), ('A', 'Активна')], default='IA', max_length=2),
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Deleted')], default=1),
        ),
    ]
