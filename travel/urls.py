from django.urls import include, path
from rest_framework.routers import DefaultRouter

from travel.views import PermitFromView, PermitView

app_name = "travel"

# Register routes
router = DefaultRouter()

api_urlpatterns = [
    path(
        "",
        PermitView.as_view(),
    ),
]
urlpatterns = [
    path("", PermitFromView.as_view()),
]
