# Generated by Django 5.0.4 on 2024-04-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resumes", "0002_rename_code_currency_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="api_id",
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]