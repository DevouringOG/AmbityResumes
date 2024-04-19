# Generated by Django 5.0.4 on 2024-04-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resumes", "0003_resume_api_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicant",
            name="area",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="resume",
            name="created_at",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="resume",
            name="updated_at",
            field=models.DateTimeField(),
        ),
    ]
