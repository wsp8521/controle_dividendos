# Generated by Django 5.1.5 on 2025-01-24 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0016_remove_proventos_ticket_alter_operacao_tipo_operacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metaativo',
            name='qtd_acoes',
        ),
        migrations.RemoveField(
            model_name='metaativo',
            name='qtd_fii',
        ),
        migrations.RemoveField(
            model_name='metaativo',
            name='total',
        ),
        migrations.AddField(
            model_name='metaativo',
            name='classe',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='meta_alcancada',
            field=models.IntegerField(blank=True, null=True, verbose_name='Meta anual alçancada'),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='meta_anual',
            field=models.IntegerField(blank=True, null=True, verbose_name='Meta Anual'),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='meta_geral',
            field=models.IntegerField(blank=True, null=True, verbose_name='Meta geral'),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='meta_geral_alcancada',
            field=models.IntegerField(blank=True, null=True, verbose_name='Meta geral alcançada'),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='status_anual',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Status Anual'),
        ),
        migrations.AddField(
            model_name='metaativo',
            name='status_geral',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Status Anual'),
        ),
        migrations.AlterField(
            model_name='metaativo',
            name='ano',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='proventos',
            name='id_ativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='carteira.ativos', verbose_name='Ativos'),
        ),
    ]
