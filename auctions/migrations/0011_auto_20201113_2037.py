# Generated by Django 3.0.5 on 2020-11-13 17:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201113_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='cat',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 20, 37, 16, 37409)),
        ),
    ]
