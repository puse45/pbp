import logging

from django.views.generic import FormView
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from travel.forms import PermitForm
from travel.models import Permit
from travel.serializers import PermitSerializer

# Create your views here.

logger = logging.getLogger(__file__)


class PermitView(generics.GenericAPIView):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "id",
        "country_of_origin",
        "country_of_destination",
        "date_of_travel",
    )

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context=self.get_serializer_context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if request.GET.get("id"):
                queryset = self.get_queryset().filter(pk=request.GET.get("id"))
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class PermitFromView(FormView):
    form_class = PermitForm
    template_name = "permit.html"
