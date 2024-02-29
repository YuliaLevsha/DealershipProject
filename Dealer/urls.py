from django.urls import path
from Dealer.views import *


urlpatterns = [
    path("get-dealers/", DealerViewSet.as_view({"get": "list"}), name="get_dealers"),
    path("get-cars/", CarViewSet.as_view({"get": "list"}), name="get_cars"),
    path(
        "get-dealers-cars/",
        DealerCarsViewSet.as_view({"get": "list"}),
        name="get_dealers_cars",
    ),
]
