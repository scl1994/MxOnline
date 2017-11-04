# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='need_know',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='you_get',
            field=models.CharField(default='', max_length=300, verbose_name='课程收获'),
        ),
    ]
