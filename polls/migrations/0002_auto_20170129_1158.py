# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='question',
            new_name='questions',
        ),
    ]
