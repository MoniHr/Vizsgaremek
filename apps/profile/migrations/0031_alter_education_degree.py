# Generated by Django 4.2.3 on 2024-08-06 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0030_remove_profile_cover_letter_remove_profile_cv"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="degree",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="education_degree",
                to="profile.educationchoice",
            ),
        ),
    ]
