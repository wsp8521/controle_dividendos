# Generated by Django 5.1.5 on 2025-01-19 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0009_operacao_ano_proventos_ano_proventos_mes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacao',
            name='data_operacao',
            field=models.DateField(verbose_name='data da operação'),
        ),
        migrations.AlterField(
            model_name='proventos',
            name='data_pgto',
            field=models.DateField(verbose_name='data do pagamento'),
        ),
    ]
