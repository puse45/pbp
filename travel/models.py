import datetime

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from base.models import BaseModel
from travel.validators import (age_of_traveller_limit,
                               validate_maximum_date_of_travel,
                               validate_minimum_date_of_travel,
                               validate_weekday)


class Permit(BaseModel):
    date_of_travel = models.DateField(
        null=False,
        blank=False,
        validators=[
            validate_weekday,
            validate_minimum_date_of_travel,
            validate_maximum_date_of_travel,
        ],
    )
    date_of_return = models.DateField(null=True, blank=True)
    country_of_origin = CountryField(
        null=False, blank=False, blank_label="(select country of origin)"
    )
    country_of_destination = CountryField(
        null=False, blank=False, blank_label="(select country of destination)"
    )
    age_of_traveller = models.PositiveIntegerField(
        null=False, blank=False, validators=[age_of_traveller_limit]
    )
    is_supervised = models.BooleanField(default=False)
    slug = False

    def __unicode__(self):
        return "Permit"

    def clean(self):
        if self.date_of_return:
            latest_date_of_return = self.date_of_travel + datetime.timedelta(days=60)
            if self.date_of_return >= latest_date_of_return:
                raise ValidationError(
                    {
                        "date_of_return": _(
                            f"Date of return for traveller must be less than {str(latest_date_of_return)}"
                        )
                    }
                )
        if self.age_of_traveller < 21 and not self.is_supervised:
            raise ValidationError(
                {
                    "is_supervised": _(
                        "Traveller less than 21 years of age must travel with the supervision of an adult"
                    )
                }
            )

        if self.country_of_origin == self.country_of_destination:
            raise ValidationError(
                {
                    "country_of_destination": _(
                        f"Traveller cannot travel to the same country of origin i.e. {self.country_of_origin.name}"
                    )
                }
            )

        country_of_origin_data = self.country_covid_data(
            country=self.country_of_origin.code.lower()
        )
        country_of_destination_data = self.country_covid_data(
            country=self.country_of_destination.code.lower()
        )
        if not isinstance(country_of_origin_data, list):
            raise ValidationError(
                {
                    "country_of_origin": _(
                        f"Covid Data {country_of_origin_data.get('message')}"
                    )
                }
            )
        if not isinstance(country_of_destination_data, list):
            raise ValidationError(
                {
                    "country_of_destination": _(
                        f"Covid Data {country_of_destination_data.get('message')}"
                    )
                }
            )
        if country_of_origin_data[0].get("Cases") > country_of_destination_data[0].get(
            "Cases"
        ):
            raise ValidationError(
                {
                    "country_of_destination": _(
                        f"Sorry traveller cannot travel from {self.country_of_origin.name} to {self.country_of_destination.name} because the number of Covid cases in the Country of origin  is higher than in the Country of destination by {int(country_of_origin_data[0].get('Cases')) - int(country_of_destination_data[0].get('Cases'))}."
                    )
                }
            )

    def country_covid_data(self, country, status="confirmed"):
        to_date = datetime.datetime.strftime(
            datetime.datetime.today(), "%Y-%m-%dT00:00:00Z"
        )
        from_date = datetime.datetime.strptime(
            to_date, "%Y-%m-%dT00:00:00Z"
        ) - datetime.timedelta(days=1)
        url = f"{settings.CORONA_VIRUS_API_BASE_URL}/total/country/{country}/status/{status}"
        payload = {"from": from_date, "to": to_date}
        headers = {
            "Authorization": f"Basic {settings.CORONA_VIRUS_API_AUTHORIZATION_TOKEN}"
        }
        return requests.get(url, headers=headers, params=payload).json()

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Travel Permit")
        verbose_name_plural = _("Travel Permit")

    def __str__(self):
        return f"{self.country_of_origin} - {self.country_of_destination} - {self.created_at}"
