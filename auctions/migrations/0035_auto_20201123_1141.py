# Generated by Django 3.0.5 on 2020-11-23 08:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0034_auto_20201122_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 23, 11, 41, 1, 301642)),
        ),
    ]