# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 18:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_task', models.CharField(max_length=45)),
                ('my_date', models.DateField()),
                ('my_time', models.TimeField()),
                ('my_status', models.TextField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('myuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myuser', to='appointments.User')),
            ],
        ),
    ]
