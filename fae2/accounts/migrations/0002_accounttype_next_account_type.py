# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-13 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttype',
            name='next_account_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_account_type', to='accounts.AccountType'),
        ),
    ]