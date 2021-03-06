# Generated by Django 3.0.5 on 2020-11-29 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0043_auto_20201129_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_img',
            field=models.URLField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cm_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 19, 36, 34, 613957)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 19, 36, 34, 613957)),
        ),
    ]
