# Generated by Django 3.0.5 on 2020-12-03 22:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0047_auto_20201129_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cm_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 4, 2, 5, 40, 186869)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 4, 2, 5, 40, 185848)),
        ),
    ]
