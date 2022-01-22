from django.urls import include, path
from rest_framework.routers import DefaultRouter

from travel.urls import api_urlpatterns as travel_urls

router = DefaultRouter()
app_name = "api"


urlpatterns = [
    path("", include(router.urls)),
    path("travel/", include(travel_urls)),
]
