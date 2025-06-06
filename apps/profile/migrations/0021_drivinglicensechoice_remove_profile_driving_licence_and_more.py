# Generated by Django 4.2.3 on 2024-08-02 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0020_languagechoice_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DrivingLicenseChoice",
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
                ("code", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name="profile",
            name="driving_licence",
        ),
        migrations.AddField(
            model_name="profile",
            name="driving_license",
            field=models.ManyToManyField(blank=True, to="profile.drivinglicensechoice"),
        ),
    ]
