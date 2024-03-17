from Dealer.models import *
from rest_framework import serializers


class DealerSerializer(
    serializers.ModelSerializer
):  
    """сериализатор модели Dealer (поставщик)"""
    customers_count = serializers.StringRelatedField()
    dealer_cars = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dealer
        fields = ("name", "foundation_year", "customers_count", "dealer_cars")


class CarModelSerializer(
    serializers.ModelSerializer
):  
    """сериализатор модели CarModel (марка машины)"""
    class Meta:
        model = CarModel
        fields = ("name",)


class CarSerializer(serializers.ModelSerializer):  
    """сериализатор модели Car (машина)"""
    car_model = CarModelSerializer()

    class Meta:
        model = Car
        fields = (
            "car_model",
            "car_year",
            "car_color",
            "number_of_doors",
            "body_type",
            "type_drive",
            "country",
            "volume_fuel_tank",
        )


class DealerCarsSerializer(
    serializers.ModelSerializer
):  
    """сериализатор модели DealerCars (машины поставщика)"""
    dealer = DealerSerializer()
    car = CarSerializer()
    price = serializers.CharField()

    class Meta:
        model = DealerCars
        fields = ("dealer", "car", "price")
