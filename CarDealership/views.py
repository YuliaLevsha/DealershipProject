from CarDealership.serializers import *
from rest_framework import mixins, status, viewsets, permissions
from django.http import HttpRequest
from typing import Any
from rest_framework.response import Response
from django.db.models import Q


class CarDealershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = CarDealership.objects.all()
    serializer_class = CarDealershipSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        name_value = self.request.GET.get("name")
        location_value = self.request.GET.get("location")

        order_value = self.request.GET.get("order")

        q_filter = Q()

        if location_value and name_value:
            q_filter = Q(name__icontains=name_value) & Q(location=location_value)
        elif name_value:
            q_filter |= Q(name__icontains=name_value)
        elif location_value:
            q_filter |= Q(location=location_value)

        if q_filter:
            queryset = queryset.filter(q_filter)

        if order_value:
            queryset = queryset.order_by(order_value)

        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        car_dealership_serializer = CarDealershipSerializer(quaryset, many=True)
        return Response(car_dealership_serializer.data, status=status.HTTP_200_OK)


class AvailableCarModelsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AvailableCarModels.objects.all()
    serializer_class = AvailableCarModelsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        car_model_name_value = self.request.GET.get("car_model")
        dealership_name_value = self.request.GET.get("dealership")

        order_value = self.request.GET.get("order")

        q_filter = Q()

        if car_model_name_value and dealership_name_value:
            q_filter = Q(car_model__name__icontains=car_model_name_value) & Q(
                car_dealership__name__icontains=dealership_name_value
            )
        elif car_model_name_value:
            q_filter |= Q(car_model__name__icontains=car_model_name_value)
        elif dealership_name_value:
            q_filter |= Q(car_dealership__name__icontains=dealership_name_value)

        if q_filter:
            queryset = queryset.filter(q_filter)

        if order_value:
            queryset = queryset.order_by(order_value)

        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        available_car_model_serializer = AvailableCarModelsSerializer(
            quaryset, many=True
        )
        return Response(available_car_model_serializer.data, status=status.HTTP_200_OK)
