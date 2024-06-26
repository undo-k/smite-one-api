# Generated by Django 4.2.7 on 2023-11-20 03:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smiteinfo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Assassin", "Assassin"),
                            ("Guardian", "Guardian"),
                            ("Hunter", "Hunter"),
                            ("Mage", "Mage"),
                            ("Warrior", "Warrior"),
                        ],
                        max_length=64,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="champion",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
