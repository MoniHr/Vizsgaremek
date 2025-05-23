# Generated by Django 4.2.3 on 2024-07-10 13:13

import apps.profile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0010_alter_education_degree"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=apps.profile.models.upload_to_profile_folder,
            ),
        ),
        migrations.AlterField(
            model_name="education",
            name="degree",
            field=models.CharField(
                choices=[
                    ("BSC", "Bsc"),
                    ("ELEMENTARY", "Elementary"),
                    ("HIGHSCHOOL", "HighSchool"),
                    ("MSC", "Msc"),
                    ("PHD", "Phd"),
                    ("SECONDARY", "Secondary"),
                ],
                help_text="Ex. Bachelor's",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="driving_licence",
            field=models.TextField(
                blank=True,
                choices=[
                    ("A", "A"),
                    ("A1", "A1"),
                    ("B", "B"),
                    ("BE", "BE"),
                    ("C1", "C1"),
                    ("C1E", "C1E"),
                    ("CE", "CE"),
                    ("D", "D"),
                    ("D1", "D1"),
                    ("D1E", "D1E"),
                    ("DE", "DE"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="work_schedule",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CONTINUOUS WORKING TIME", "Continuous Working Time"),
                    ("FLEXIBLE", "Flexible"),
                    (
                        "FOR CHANGED EMPLOYMENT CAPACITY",
                        "For Changed Employment Capacity",
                    ),
                    ("GENERAL WORKING SCHEDULE", "General Working Schedule"),
                    (
                        "IN PENSION, WORK NEXT TO RETIRED",
                        "In Pension, Work Next To Retired",
                    ),
                    (
                        "FOR MOTHERS AND/OR SINGLE PARENTS",
                        "For Mothers And/or Single Parents",
                    ),
                    ("OPTIONAL WORKING HOURS", "Optional Working Hours"),
                    ("2 SHIFTS", "2 Shifts"),
                    ("3 SHIFTS", "3 Shifts"),
                    ("12/24 SHIFT", "12/24 Shifts"),
                    ("12/48 SHIFT", "12/48 Shifts"),
                    ("24/72 SHIFT, STANDBY SERVICE", "24/72 Shift, Standby Service"),
                    ("STUDENT WORK", "Student Work"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="working_time",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CASUAL", "Casual"),
                    (
                        "FOR CHANGED EMPLOYMENT CAPACITY",
                        "For changed employment capacity",
                    ),
                    (
                        "FOR MOTHERS AND / OR SINGLE PARENTS",
                        "For Mothers and / or Single Parents",
                    ),
                    ("FULL TIME", "Full time"),
                    ("HOME OFFICE", "Home office"),
                    (
                        "IN PENSION, WORK NEXT TO RETIRED",
                        "In pension, work next to retired",
                    ),
                    ("PART TIME", "Part time"),
                    ("PROFESSIONAL PRACTICE", "Professional practice"),
                    ("REMOTE WORK", "Remote work"),
                    ("STUDENT WORK", "Student work"),
                ],
                null=True,
            ),
        ),
    ]
