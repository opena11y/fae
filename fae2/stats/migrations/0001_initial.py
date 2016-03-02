# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('websiteResultGroups', '0001_initial'),
        ('rulesets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsAll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ws_report_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup')),
            ],
            options={
                'verbose_name': 'Stats All',
                'verbose_name_plural': 'Stats All',
            },
        ),
        migrations.CreateModel(
            name='StatsDay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('day', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-stats_month', '-day'],
                'verbose_name': 'Stats Day',
                'verbose_name_plural': 'Stats Day',
            },
        ),
        migrations.CreateModel(
            name='StatsMonth',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-stats_year', '-month'],
                'verbose_name': 'Stats Month',
                'verbose_name_plural': 'Stats Months',
            },
        ),
        migrations.CreateModel(
            name='StatsRegisteredUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Stats Registered Users',
                'verbose_name_plural': 'Stats Registered Users',
            },
        ),
        migrations.CreateModel(
            name='StatsRuleset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ruleset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='rulesets.Ruleset')),
                ('stats_all', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rulesets', to='stats.StatsAll')),
                ('ws_report_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup')),
            ],
            options={
                'ordering': ['ruleset'],
                'verbose_name': 'Stats Ruleset',
                'verbose_name_plural': 'Stats Rulesets',
            },
        ),
        migrations.CreateModel(
            name='StatsUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to=settings.AUTH_USER_MODEL)),
                ('ws_report_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup')),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Stats User',
                'verbose_name_plural': 'Stats User',
            },
        ),
        migrations.CreateModel(
            name='StatsYear',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(default=2016)),
                ('stats_all', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='years', to='stats.StatsAll')),
                ('ws_report_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup')),
            ],
            options={
                'ordering': ['-year'],
                'verbose_name': 'Stats Year',
                'verbose_name_plural': 'Stats Years',
            },
        ),
        migrations.AddField(
            model_name='statsregisteredusers',
            name='user_stats',
            field=models.ManyToManyField(blank=True, default=None, related_name='stats_registered_users', to='stats.StatsUser'),
        ),
        migrations.AddField(
            model_name='statsregisteredusers',
            name='ws_report_group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup'),
        ),
        migrations.AddField(
            model_name='statsmonth',
            name='stats_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='stats.StatsYear'),
        ),
        migrations.AddField(
            model_name='statsmonth',
            name='ws_report_group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup'),
        ),
        migrations.AddField(
            model_name='statsday',
            name='stats_month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='stats.StatsMonth'),
        ),
        migrations.AddField(
            model_name='statsday',
            name='ws_report_group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='websiteResultGroups.WebsiteReportGroup'),
        ),
    ]
