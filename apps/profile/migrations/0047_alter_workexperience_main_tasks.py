# Generated by Django 4.2.3 on 2024-11-06 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0046_alter_education_options_alter_workexperience_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workexperience",
            name="main_tasks",
            field=models.TextField(blank=True, null=True),
        ),
    ]
