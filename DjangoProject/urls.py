from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import routers
from Customer.urls import urlpatterns as customer_router
from Dealer.urls import urlpatterns as dealer_router
from CarDealership.urls import urlpatterns as dealership_router


common_url = []
common_url.extend(customer_router)
common_url.extend(dealer_router)
common_url.extend(dealership_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(common_url)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
