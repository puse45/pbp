from django.contrib import admin

# Register your models here.
from travel.models import Permit


class PermitAdmin(admin.ModelAdmin):
    list_display = (
        "date_of_travel",
        "date_of_return",
        "country_of_origin",
        "country_of_destination",
        "age_of_traveller",
        "is_supervised",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "country_of_origin",
        "country_of_destination",
        "is_supervised",
        "created_at",
        "country_of_destination",
    )
    list_per_page = 20


admin.site.register(Permit, PermitAdmin)