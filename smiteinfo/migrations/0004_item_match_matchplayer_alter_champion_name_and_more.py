# Generated by Django 4.2.7 on 2023-11-21 19:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("smiteinfo", "0003_delete_role_champion_damage_type_champion_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(max_length=64, unique=True)),
                (
                    "tier",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                (
                    "game_mode",
                    models.CharField(
                        choices=[
                            ("Arena", "Arena"),
                            ("Assault", "Assault"),
                            ("Conquest", "Conquest"),
                            ("Joust", "Joust"),
                            ("Slash", "Slash"),
                        ],
                        max_length=64,
                    ),
                ),
                ("match_date", models.DateField()),
                (
                    "winning_team",
                    models.CharField(
                        choices=[("Chaos", "Chaos"), ("Order", "Order")], max_length=64
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MatchPlayer",
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
                    "team",
                    models.CharField(
                        choices=[("Chaos", "Chaos"), ("Order", "Order")], max_length=64
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="champion",
            name="name",
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="champion",
            name="role",
            field=models.CharField(
                choices=[
                    ("Assassin", "Assassin"),
                    ("Guardian", "Guardian"),
                    ("Hunter", "Hunter"),
                    ("Mage", "Mage"),
                    ("Warrior", "Warrior"),
                ],
                max_length=64,
            ),
        ),
        migrations.CreateModel(
            name="MatchPlayerDetails",
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
                ("kills", models.PositiveIntegerField()),
                ("deaths", models.PositiveIntegerField()),
                ("assists", models.PositiveIntegerField()),
                ("gold", models.PositiveIntegerField()),
                ("player_damage", models.PositiveIntegerField()),
                ("minion_damage", models.PositiveIntegerField()),
                ("damage_taken", models.PositiveIntegerField()),
                ("damage_mitigated", models.PositiveIntegerField()),
                ("structure_damage", models.PositiveIntegerField()),
                ("player_healing", models.PositiveIntegerField()),
                (
                    "match_player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="smiteinfo.matchplayer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="matchplayer",
            name="god",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="smiteinfo.champion"
            ),
        ),
        migrations.AddField(
            model_name="matchplayer",
            name="items",
            field=models.ManyToManyField(to="smiteinfo.item"),
        ),
        migrations.AddField(
            model_name="matchplayer",
            name="match",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="smiteinfo.match"
            ),
        ),
    ]
