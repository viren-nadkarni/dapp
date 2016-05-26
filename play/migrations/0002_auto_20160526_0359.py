# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playapp',
            name='id',
        ),
        migrations.AlterField(
            model_name='playapp',
            name='app_id',
            field=models.CharField(max_length=256, serialize=False, primary_key=True),
        ),
    ]
