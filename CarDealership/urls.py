from django.urls import path
from CarDealership.views import *


urlpatterns = [
    path(
        "get-dealerships/",
        CarDealershipViewSet.as_view({"get": "list"}),
        name="get_car_dealerships",
    ),
    path(
        "get-available-models/",
        AvailableCarModelsViewSet.as_view({"get": "list"}),
        name="get_available_models",
    ),
]
