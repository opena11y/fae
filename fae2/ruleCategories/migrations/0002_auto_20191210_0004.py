# Generated by Django 2.2.7 on 2019-12-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleCategories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rulecategory',
            name='title_plural',
            field=models.CharField(max_length=256, verbose_name='Title Plural'),
        ),
    ]