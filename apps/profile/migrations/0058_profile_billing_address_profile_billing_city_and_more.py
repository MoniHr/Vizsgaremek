# Generated by Django 5.1 on 2025-04-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0057_profile_created_at_profile_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="billing_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="billing_city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="billing_country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="billing_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="billing_tax_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="billing_zip_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
