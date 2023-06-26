# Generated by Django 4.2.2 on 2023-06-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city_name", models.CharField(max_length=500, unique=True)),
                ("lat", models.FloatField()),
                ("lon", models.FloatField()),
                ("temp", models.FloatField(blank=True, null=True)),
                ("hum", models.IntegerField(blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
