# Generated by Django 4.2.3 on 2024-03-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="company_file",
            field=models.FileField(
                null=True, upload_to='apps.accounts.models.upload_to_profile_folder'
            ),
        ),
    ]
