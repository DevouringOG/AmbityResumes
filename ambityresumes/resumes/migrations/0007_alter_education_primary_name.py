# Generated by Django 5.0.4 on 2024-04-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resumes", "0006_alter_applicant_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="primary_name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]