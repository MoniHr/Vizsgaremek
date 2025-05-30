# Generated by Django 4.2.3 on 2025-01-15 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0047_alter_workexperience_main_tasks"),
    ]

    operations = [
        migrations.AddField(
            model_name="coverletter",
            name="language",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profile.languagechoice",
            ),
        ),
        migrations.AddField(
            model_name="cv",
            name="language",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profile.languagechoice",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="language",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profile.languagechoice",
            ),
        ),
    ]
