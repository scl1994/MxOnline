# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长（分钟数）'),
        ),
    ]
