# Generated by Django 5.1.5 on 2025-04-12 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0037_setorativo_fk_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setorativo',
            name='fk_user',
        ),
    ]
