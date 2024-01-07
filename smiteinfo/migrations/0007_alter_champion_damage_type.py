# Generated by Django 4.2.7 on 2023-11-21 20:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smiteinfo", "0006_alter_champion_damage_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="champion",
            name="damage_type",
            field=models.CharField(
                blank=True,
                choices=[("Magical", "Magical"), ("Physical", "Physical")],
                max_length=64,
            ),
        ),
    ]