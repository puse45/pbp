# Generated by Django 3.2 on 2022-01-22 10:50

from django.db import migrations, models

import travel.validators


class Migration(migrations.Migration):

    dependencies = [
        ("travel", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permit",
            name="age_of_traveller",
            field=models.PositiveIntegerField(
                validators=[travel.validators.age_of_traveller_limit]
            ),
        ),
        migrations.AlterField(
            model_name="permit",
            name="date_of_travel",
            field=models.DateField(
                validators=[
                    travel.validators.validate_weekday,
                    travel.validators.validate_minimum_date_of_travel,
                    travel.validators.validate_maximum_date_of_travel,
                ]
            ),
        ),
    ]
