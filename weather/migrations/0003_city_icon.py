# Generated by Django 4.2.2 on 2023-07-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0002_forecast"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="icon",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
