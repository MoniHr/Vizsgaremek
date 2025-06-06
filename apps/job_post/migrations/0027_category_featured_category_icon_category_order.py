# Generated by Django 4.2.3 on 2024-08-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_post", "0026_alter_jobpost_category_alter_jobpost_sub_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
