import datetime

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from travel.models import Permit


def country_covid_data(country, status="confirmed"):
    to_date = datetime.datetime.strftime(
        datetime.datetime.today(), "%Y-%m-%dT00:00:00Z"
    )
    from_date = datetime.datetime.strptime(
        to_date, "%Y-%m-%dT00:00:00Z"
    ) - datetime.timedelta(days=1)
    url = (
        f"{settings.CORONA_VIRUS_API_BASE_URL}/total/country/{country}/status/{status}"
    )
    payload = {"from": from_date, "to": to_date}
    headers = {
        "Authorization": f"Basic {settings.CORONA_VIRUS_API_AUTHORIZATION_TOKEN}"
    }
    return requests.get(url, headers=headers, params=payload).json()


class PermitSerializer(serializers.ModelSerializer):
    country_of_origin = CountryField(country_dict=True)
    country_of_destination = CountryField(country_dict=True)

    class Meta:
        model = Permit
        fields = (
            "id",
            "date_of_travel",
            "date_of_return",
            "country_of_origin",
            "country_of_destination",
            "age_of_traveller",
            "is_supervised",
        )

    def validate(self, attrs):
        print(attrs)
        date_of_travel = attrs.get("date_of_travel", None)
        date_of_return = attrs.get("date_of_return", None)
        country_of_origin = attrs.get("country_of_origin", None)
        country_of_destination = attrs.get("country_of_destination", None)
        age_of_traveller = attrs.get("age_of_traveller", None)
        is_supervised = attrs.get("is_supervised", None)

        if date_of_return:
            latest_date_of_return = date_of_travel + datetime.timedelta(days=60)
            if date_of_return >= latest_date_of_return:
                raise serializers.ValidationError(
                    {
                        "date_of_return": _(
                            f"Date of return for traveller must be less than {str(latest_date_of_return)}"
                        )
                    }
                )
        if age_of_traveller < 21 and not is_supervised:
            raise serializers.ValidationError(
                {
                    "is_supervised": _(
                        "Traveller less than 21 years of age must travel with the supervision of an adult"
                    )
                }
            )

        if country_of_origin == country_of_destination:
            raise serializers.ValidationError(
                {
                    "country_of_destination": _(
                        f"Traveller cannot travel to the same country of origin i.e. {country_of_origin}"
                    )
                }
            )

        country_of_origin_data = country_covid_data(country=country_of_origin.lower())
        country_of_destination_data = country_covid_data(
            country=country_of_destination.lower()
        )
        if not isinstance(country_of_origin_data, list):
            raise serializers.ValidationError(
                {
                    "country_of_origin": _(
                        f"Covid Data {country_of_origin_data.get('message')}"
                    )
                }
            )

        if not isinstance(country_of_destination_data, list):
            raise serializers.ValidationError(
                {
                    "country_of_destination": _(
                        f"Covid Data {country_of_destination_data.get('message')}"
                    )
                }
            )
        if not country_of_origin_data:
            raise serializers.ValidationError(
                {"country_of_origin": _("Covid Data not found")}
            )
        if not country_of_destination_data:
            raise serializers.ValidationError(
                {"country_of_destination": _("Covid Data not found")}
            )
        if country_of_origin_data[0].get("Cases") > country_of_destination_data[0].get(
            "Cases"
        ):
            raise serializers.ValidationError(
                {
                    "country_of_destination": _(
                        f"Sorry traveller cannot travel from {country_of_origin} to {country_of_destination} because the number of Covid cases in the Country of origin  is higher than in the Country of destination by {int(country_of_origin_data[0].get('Cases')) - int(country_of_destination_data[0].get('Cases'))}."
                    )
                }
            )

        return attrs
