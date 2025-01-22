# Generated by Django 5.1.5 on 2025-01-22 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0012_proventos_id_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacao',
            name='id_ativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='carteira.ativos'),
        ),
    ]
