# Generated by Django 4.2.2 on 2023-08-05 06:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0008_alter_city_unique_together_city_unique_location"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="city",
            name="unique location",
        ),
    ]
