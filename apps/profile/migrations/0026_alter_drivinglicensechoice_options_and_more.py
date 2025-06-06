# Generated by Django 4.2.3 on 2024-08-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0025_alter_employmentschedulechoice_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="drivinglicensechoice",
            options={
                "verbose_name": "Driving License Choice",
                "verbose_name_plural": "Driving License Choices",
            },
        ),
        migrations.AlterModelOptions(
            name="educationchoice",
            options={
                "verbose_name": "Education Choice",
                "verbose_name_plural": "Education Choices",
            },
        ),
        migrations.AlterModelOptions(
            name="joblocationchoice",
            options={
                "verbose_name": "Job Location Choice",
                "verbose_name_plural": "Job Location Choices",
            },
        ),
        migrations.AlterModelOptions(
            name="languagechoice",
            options={
                "verbose_name": "Language Choice",
                "verbose_name_plural": "Language Choices",
            },
        ),
        migrations.AlterModelOptions(
            name="workingtimechoice",
            options={
                "verbose_name": "Working Time Choice",
                "verbose_name_plural": "Working Time Choices",
            },
        ),
        migrations.AddField(
            model_name="drivinglicensechoice",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="drivinglicensechoice",
            name="name_hu",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="educationchoice",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="educationchoice",
            name="name_hu",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="joblocationchoice",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="joblocationchoice",
            name="name_hu",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="languagechoice",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="languagechoice",
            name="name_hu",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="workingtimechoice",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="workingtimechoice",
            name="name_hu",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
