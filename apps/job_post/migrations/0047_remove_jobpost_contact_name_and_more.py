# Generated by Django 5.1 on 2025-04-09 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("job_post", "0046_alter_jobpost_stripe_checkout_session_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jobpost",
            name="contact_name",
        ),
        migrations.RemoveField(
            model_name="jobpost",
            name="is_contact_name_public",
        ),
    ]
