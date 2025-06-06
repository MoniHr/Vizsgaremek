# Generated by Django 4.2.3 on 2024-04-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0016_rename__company_user_rel_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[
                    ("HUNGARIAN", "hungarian"),
                    ("ENGLISH", "english"),
                    ("GERMAN", "german"),
                    ("DUTCH", "dutch"),
                ],
                default="ENGLISH",
            ),
        ),
    ]
