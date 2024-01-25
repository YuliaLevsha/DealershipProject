from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from djmoney.models.fields import MoneyField
from base_model import BaseModel, G8Countries


class CarDealership(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Car dealership name")
    country = CountryField(countries=G8Countries, verbose_name="Car dealership country")
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car dealership balance",
    )
    description_cars = models.JSONField(
        encoder=None, decoder=None, verbose_name="Description future cars to sale"
    )
    dealership_cars = models.ManyToManyField(
        "Dealer.DealerCars",
        through="CarDealershipDealersCar",
        verbose_name="List cars to sale",
    )
    list_models = models.ManyToManyField(
        "Dealer.CarModel",
        through="CarDealershipModel",
        verbose_name="Models to sale",
        related_name="car_dealerships",
    )

    class Meta:
        db_table = "car_dealership"
        verbose_name = "CarDealership"


class Discount(BaseModel):
    start_date = models.DateTimeField(verbose_name="Start discount")
    finish_date = models.DateTimeField(verbose_name="Finish discount")
    percent = models.PositiveIntegerField(
        validators=[MaxValueValidator(50)], verbose_name="Percent discount"
    )
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="discounts",
        verbose_name="Discount for car dealership",
    )
    name = models.CharField(max_length=255, verbose_name="Discount name")
    description = models.CharField(max_length=255, verbose_name="Discount description")

    class Meta:
        db_table = "discounts"
        verbose_name = "Discounts"


class CarDealershipModel(BaseModel):
    car_model = models.ForeignKey(
        "Dealer.CarModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Model of car",
    )
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_car_model",
        verbose_name="Car dealership",
    )

    class Meta:
        db_table = "car_dealership_model"
        verbose_name = "CarDealershipModel"


class CarDealershipDealersCar(BaseModel):
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_cars",
        verbose_name="Car dealership which buy car",
    )
    dealer_car = models.ForeignKey(
        "Dealer.DealerCars",
        on_delete=models.SET_NULL,
        null=True,
        related_name="history",
        verbose_name="Dealer car which was bought",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Discount for bought",
    )
    new_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price in dealership",
    )

    class Meta:
        db_table = "car_dealership_dealer_car"
        verbose_name = "CarDealershipDealersCar"
