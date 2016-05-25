# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_id', models.CharField(max_length=256)),
                ('app_name', models.CharField(max_length=256)),
                ('dev_name', models.CharField(max_length=256)),
                ('dev_email', models.EmailField(max_length=254)),
                ('icon_url', models.URLField()),
            ],
        ),
    ]
