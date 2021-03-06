# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-19 04:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_mutualfunds'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mutualfunds',
            old_name='beginning_assets',
            new_name='finalfunds',
        ),
        migrations.RenameField(
            model_name='mutualfunds',
            old_name='ending_assets',
            new_name='initialfunds',
        ),
        migrations.RenameField(
            model_name='mutualfunds',
            old_name='net_flow',
            new_name='resultant',
        ),
        migrations.RenameField(
            model_name='mutualfunds',
            old_name='created_date',
            new_name='start_date',
        ),
    ]
