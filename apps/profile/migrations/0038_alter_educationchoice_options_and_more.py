# Generated by Django 4.2.3 on 2024-10-21 10:53

import apps.profile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0037_remove_profile_number_of_employees"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="educationchoice",
            options={
                "ordering": ["custom_order"],
                "verbose_name": "Education Choice",
                "verbose_name_plural": "Education Choices",
            },
        ),
        migrations.AlterModelOptions(
            name="subactivity",
            options={
                "verbose_name": "Subactivity",
                "verbose_name_plural": "Subactivities",
            },
        ),
        migrations.AddField(
            model_name="educationchoice",
            name="custom_order",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="company_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=apps.profile.models.upload_to_profile_folder,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="company_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=apps.profile.models.upload_to_profile_folder,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
