# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-21 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tripsched', '0004_auto_20180521_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='Enddate',
            field=models.DateField(),
        ),
    ]
