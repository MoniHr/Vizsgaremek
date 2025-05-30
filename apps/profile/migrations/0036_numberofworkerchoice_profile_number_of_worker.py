# Generated by Django 4.2.3 on 2024-08-07 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0035_remove_profile_main_of_activity_profile_activity_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="NumberOfWorkerChoice",
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
                ("name_en", models.CharField(max_length=255, null=True)),
                ("name_hu", models.CharField(max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Number Of Worker Choice",
                "verbose_name_plural": "Number Of Workers Choices",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="number_of_worker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profile.numberofworkerchoice",
            ),
        ),
    ]
