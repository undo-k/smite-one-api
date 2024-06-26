# Generated by Django 4.2.7 on 2023-11-21 20:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smiteinfo", "0005_rename_matchplayerdetails_matchplayerdetail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="champion",
            name="damage_type",
            field=models.CharField(
                blank=True,
                choices=[("Magical", "Magical"), ("Physical", "Physical")],
                max_length=64,
                unique=True,
            ),
        ),
    ]
