# Generated by Django 5.1.5 on 2025-01-25 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0018_alter_metaativo_status_anual_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metaativo',
            name='status_anual',
        ),
        migrations.RemoveField(
            model_name='metaativo',
            name='status_geral',
        ),
    ]
