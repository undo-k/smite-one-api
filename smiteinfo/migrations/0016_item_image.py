# Generated by Django 4.2.7 on 2023-12-10 20:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smiteinfo", "0015_alter_match_banned_gods"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="image",
            field=models.ImageField(null=True, upload_to="images/"),
        ),
    ]
