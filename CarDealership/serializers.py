import Dealer.serializers
from CarDealership.models import *
from rest_framework import serializers


class CarDealershipSerializer(
    serializers.ModelSerializer
):  # сериализатор модели CarDealership (автосалон)
    dealership_cars = serializers.StringRelatedField(many=True)
    car_models = serializers.StringRelatedField(many=True)
    description_cars = serializers.JSONField()
    balance = serializers.CharField()

    class Meta:
        model = CarDealership
        fields = (
            "name",
            "location",
            "balance",
            "description_cars",
            "car_models",
            "dealership_cars",
        )


class AvailableCarModelsSerializer(serializers.ModelSerializer):
    # сериализатор для модели AvailableCarModels (модели, которые продает салон)
    car_model = Dealer.serializers.CarModelSerializer()
    car_dealership = CarDealershipSerializer()

    class Meta:
        model = AvailableCarModels
        fields = ("car_model", "car_dealership")
