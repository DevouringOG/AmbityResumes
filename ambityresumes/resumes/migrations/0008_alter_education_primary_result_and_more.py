# Generated by Django 5.0.4 on 2024-04-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resumes", "0007_alter_education_primary_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="primary_result",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="education",
            name="primary_year",
            field=models.PositiveIntegerField(null=True),
        ),
    ]