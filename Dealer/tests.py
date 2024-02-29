from django.test import TestCase
from rest_framework.test import APIClient
from Dealer.models import *


class GetListItemsTestCase(TestCase):
    def setUp(self) -> None:
        self.dealer = Dealer.objects.create(name="testname", foundation_year=2020)
        self.client = APIClient()

    def test_get_dealers(self) -> None:
        response = self.client.get("/api/get-dealers/")
        self.assertEquals(response.status_code, 200)
