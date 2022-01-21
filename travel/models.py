from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from django_countries.fields import CountryField

from base.models import BaseModel
from travel.validators import validate_weekday, validate_minimum_date_of_travel, validate_maximum_date_of_travel


class Permit(BaseModel):
    date_of_travel = models.DateField(null=False,blank=False,validators=[validate_weekday,validate_minimum_date_of_travel,validate_maximum_date_of_travel])
    date_of_return = models.DateField(null=True,blank=True)
    country_of_origin = CountryField(null=False,blank=False)
    country_of_destination = CountryField(null=False,blank=False)
    age_of_traveller = models.PositiveIntegerField(null=False,blank=False)
    is_supervised = models.BooleanField(default=False)
    slug = False

    def __unicode__(self):
        return "Permit"

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Travel Permit")
        verbose_name_plural = _("Travel Permit")

    def __str__(self):
        return f"{self.country_of_origin} - {self.country_of_destination} - {self.created_at}"
