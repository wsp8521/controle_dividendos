# Generated by Django 5.1.5 on 2025-04-09 00:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0033_ativos_corretora'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentabilidade',
            name='id_ativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carteira.ativos', verbose_name='Ativo'),
        ),
    ]
