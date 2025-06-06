# Generated by Django 5.1.7 on 2025-03-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('phone', models.CharField(max_length=20, verbose_name='الهاتف')),
                ('whatsapp_link', models.URLField(verbose_name='رابط واتساب')),
                ('address', models.CharField(max_length=255, verbose_name='العنوان')),
            ],
        ),
    ]
