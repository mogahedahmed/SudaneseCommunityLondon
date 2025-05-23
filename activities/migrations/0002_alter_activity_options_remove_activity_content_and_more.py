# Generated by Django 5.1.7 on 2025-03-25 02:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='content',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='created_at',
        ),
        migrations.AddField(
            model_name='activity',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ النشاط'),
        ),
        migrations.AddField(
            model_name='activity',
            name='description',
            field=models.TextField(default='لا يوجد وصف بعد', verbose_name='تفاصيل النشاط'),
            preserve_default=False,
        ),
    ]
