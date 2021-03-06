# Generated by Django 3.0.5 on 2020-11-13 17:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201113_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 20, 40, 8, 580312)),
        ),
    ]
