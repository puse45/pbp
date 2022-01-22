from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from travel.models import Permit


# views test
class ViewsPermitTestCase(TestCase):
    def test_permit(self):
        """Closest point compute"""
        response = self.client.get("/travel/")
        self.assertEqual(response.status_code, 200)


# api test
class ViewsAPIPermitTestCase(APITestCase):
    def test_permit_create(self):
        """Permit create"""
        payload = {
            "date_of_travel": "2022-01-25",
            "date_of_return": "2022-01-25",
            "country_of_origin": "congo",
            "country_of_destination": "Kenya",
            "age_of_traveller": 22,
            "is_supervised": False,
        }

        response = self.client.post("/api/travel/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Permit.objects.count(), 1)
        self.assertEqual(
            str(Permit.objects.get().date_of_travel), payload["date_of_travel"]
        )
