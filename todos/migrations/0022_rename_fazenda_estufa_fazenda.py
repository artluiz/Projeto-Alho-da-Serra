# Generated by Django 5.0 on 2024-01-11 16:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todos", "0021_alter_produtos_descricao_alter_produtos_produto"),
    ]

    operations = [
        migrations.RenameField(
            model_name="estufa",
            old_name="Fazenda",
            new_name="fazenda",
        ),
    ]
