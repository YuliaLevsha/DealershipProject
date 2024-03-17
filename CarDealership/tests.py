from django.test import TestCase
from CarDealership.models import *
from rest_framework.test import APIClient


class GetListItemsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_dealers(self) -> None:
        response = self.client.get("/api/get-dealerships/")
        self.assertEquals(response.status_code, 200)
