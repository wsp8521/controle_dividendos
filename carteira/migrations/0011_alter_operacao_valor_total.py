# Generated by Django 5.1.5 on 2025-01-19 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carteira', '0010_alter_operacao_data_operacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacao',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Total da Operaçao'),
        ),
    ]
