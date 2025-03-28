# Generated by Django 5.1.7 on 2025-03-24 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_familymember'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='can_vote',
            field=models.CharField(choices=[('نعم', 'نعم'), ('لا', 'لا')], default='نعم', max_length=5, verbose_name='أحقية التصويت'),
        ),
    ]
