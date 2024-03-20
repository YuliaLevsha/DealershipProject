from Dealer.serializers import *
from rest_framework import mixins, status, viewsets, permissions
from django.http import HttpRequest
from typing import Any
from rest_framework.response import Response
from django.db.models import Q


class DealerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        name_value = self.request.GET.get("name")
        foundation_year_value = self.request.GET.get("foundation")
        customers_count_value = self.request.GET.get("customer_count")

        order_value = self.request.GET.get("order")

        q_filter = Q()

        if name_value and foundation_year_value and customers_count_value:
            q_filter = (
                Q(name__icontains=name_value)
                & Q(foundation_year=foundation_year_value)
                & Q(customers_count=customers_count_value)
            )
        elif name_value:
            q_filter |= Q(name__icontains=name_value)
        elif foundation_year_value:
            q_filter |= Q(foundation_year=foundation_year_value)
        elif customers_count_value:
            q_filter |= Q(customers_count=customers_count_value)

        if q_filter:
            queryset = queryset.filter(q_filter)

        if order_value:
            queryset = queryset.order_by(order_value)

        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        quaryset = self.get_queryset()
        dealer_serializer = DealerSerializer(quaryset, many=True)
        return Response(dealer_serializer.data, status=status.HTTP_200_OK)


class CarViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        car_model_name_value = self.request.GET.get("car_model")
        car_year_value = self.request.GET.get("year")
        car_color_value = self.request.GET.get("color")
        body_type_value = self.request.GET.get("body_type")
        type_drive_value = self.request.GET.get("type_drive")
        country_value = self.request.GET.get("country")

        order_value = self.request.GET.get("order")

        q_filter = Q()

        if (
            car_model_name_value
            and car_year_value
            and car_color_value
            and body_type_value
            and type_drive_value
            and country_value
        ):
            q_filter = (
                Q(car_model__name__icontains=car_model_name_value)
                & Q(car_year=car_year_value)
                & Q(car_color__icontains=car_color_value)
                & Q(body_type__icontains=body_type_value)
                & Q(type_drive__icontains=type_drive_value)
                & Q(country=country_value)
            )
        elif car_model_name_value:
            q_filter |= Q(car_model__name__icontains=car_model_name_value)
        elif car_year_value:
            q_filter |= Q(car_year=car_year_value)
        elif car_color_value:
            q_filter |= Q(car_color__icontains=car_color_value)
        elif body_type_value:
            q_filter |= Q(body_type__icontains=body_type_value)
        elif type_drive_value:
            q_filter |= Q(type_drive__icontains=type_drive_value)
        elif country_value:
            q_filter |= Q(country=country_value)

        if q_filter:
            queryset = queryset.filter(q_filter)

        if order_value:
            queryset = queryset.order_by(order_value)

        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        car_serializer = CarSerializer(queryset, many=True)
        return Response(car_serializer.data, status=status.HTTP_200_OK)


class DealerCarsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = DealerCars.objects.all()
    serializer_class = DealerCarsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        dealer_name_value = self.request.GET.get("dealer")
        car_model_value = self.request.GET.get("car_model")

        order_value = self.request.GET.get("order")

        q_filter = Q()

        if dealer_name_value and car_model_value:
            q_filter = Q(dealer__name__icontains=dealer_name_value) & Q(
                car__car_model__name__icontains=car_model_value
            )
        elif dealer_name_value:
            q_filter |= Q(dealer__name__icontains=dealer_name_value)
        elif car_model_value:
            q_filter |= Q(car__car_model__name__icontains=car_model_value)

        if q_filter:
            queryset = queryset.filter(q_filter)

        if order_value:
            queryset = queryset.order_by(order_value)

        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        dealer_cars__serializer = DealerCarsSerializer(queryset, many=True)
        return Response(dealer_cars__serializer.data, status=status.HTTP_200_OK)
