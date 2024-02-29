from Dealer.serializers import *
from rest_framework import mixins, status, viewsets, permissions
from django.http import HttpRequest
from typing import Any
from rest_framework.response import Response


class DealerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        dealer_serializer = DealerSerializer(quaryset, many=True)
        return Response(dealer_serializer.data, status=status.HTTP_200_OK)


class CarViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        car_serializer = CarSerializer(queryset, many=True)
        return Response(car_serializer.data, status=status.HTTP_200_OK)


class DealerCarsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = DealerCars.objects.all()
    serializer_class = DealerCarsSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        dealer_cars__serializer = DealerCarsSerializer(queryset, many=True)
        return Response(dealer_cars__serializer.data, status=status.HTTP_200_OK)
