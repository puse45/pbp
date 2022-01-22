import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_weekday(value):
    if value.weekday() > 4:
        raise ValidationError(
            _("%(value)s is not a working day"),
            params={"value": value},
        )


def validate_minimum_date_of_travel(value):
    earlies_travel_date = datetime.datetime.now().date() + datetime.timedelta(days=2)
    if value < earlies_travel_date:
        raise ValidationError(
            _(
                f"{value} must be at least 2 working days in advance i.e. {str(earlies_travel_date)}"
            ),
            params={"value": value},
        )


def validate_maximum_date_of_travel(value):
    latest_travel_date = datetime.datetime.now().date() + datetime.timedelta(days=5)
    if value > latest_travel_date:
        raise ValidationError(
            _(
                f"{value} must be less than 5 working days in advance i.e. {str(latest_travel_date)}"
            ),
            params={"value": value},
        )


def age_of_traveller_limit(value):
    if value not in range(15, 66):
        raise ValidationError(
            _(
                f"Traveller age must be at least 15 and 65 years of age and above not {value} years of age"
            ),
            params={"value": value},
        )
