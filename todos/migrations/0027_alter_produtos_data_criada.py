# Generated by Django 4.2.9 on 2024-02-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todos", "0026_alter_atividade_data_atualizado_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produtos",
            name="data_criada",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Data de criação"
            ),
        ),
    ]
