# Generated by Django 5.1.5 on 2025-01-22 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0013_operacao_id_ativo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operacao',
            name='ticket',
        ),
        migrations.AlterField(
            model_name='operacao',
            name='id_ativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='carteira.ativos', verbose_name='Ativo'),
        ),
    ]
