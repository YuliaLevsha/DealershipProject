from CarDealership.serializers import *
from rest_framework import mixins, status, viewsets, permissions
from django.http import HttpRequest
from typing import Any
from rest_framework.response import Response


class CarDealershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = CarDealership.objects.all()
    serializer_class = CarDealershipSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        car_dealership_serializer = CarDealershipSerializer(quaryset, many=True)
        return Response(car_dealership_serializer.data, status=status.HTTP_200_OK)


class AvailableCarModelsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AvailableCarModels.objects.all()
    serializer_class = AvailableCarModelsSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        available_car_model_serializer = AvailableCarModelsSerializer(
            quaryset, many=True
        )
        return Response(available_car_model_serializer.data, status=status.HTTP_200_OK)
