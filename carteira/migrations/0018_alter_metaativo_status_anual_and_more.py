# Generated by Django 5.1.5 on 2025-01-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0017_remove_metaativo_qtd_acoes_remove_metaativo_qtd_fii_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metaativo',
            name='status_anual',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Status Anual'),
        ),
        migrations.AlterField(
            model_name='metaativo',
            name='status_geral',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Status Anual'),
        ),
    ]
