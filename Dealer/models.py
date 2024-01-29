from django.db import models
from django_countries.fields import CountryField
from base_model import BaseModel, G8Countries
from django.core.validators import MaxValueValidator
from djmoney.models.fields import MoneyField


class Dealer(BaseModel):  # Поставщик
    name = models.CharField(max_length=255, verbose_name="Dealer name")
    foundation_year = models.PositiveIntegerField(
        blank=False,
        validators=[MaxValueValidator(2024)],
        verbose_name="Dealer foundation year",
    )
    customers_count = models.PositiveIntegerField(
        default=0, verbose_name="Dealer customers count"
    )
    dealer_cars = models.ManyToManyField(  # Список машин, которые продает поставщик
        "Car",
        through="DealerCars",
        verbose_name="Dealers cars to sale",
        related_name="dealers",
    )

    class Meta:
        db_table = "dealer"
        verbose_name = "Dealer"


class CarModel(BaseModel):  # Модели машин
    name = models.CharField(max_length=255, verbose_name="Name model")

    class Meta:
        db_table = "car_model"
        verbose_name = "CarModel"


class Car(BaseModel):  # Машина
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name="Car model",
        related_name="cars",
    )  # модель машины
    car_year = models.PositiveIntegerField(
        blank=False, verbose_name="Car year"
    )  # Год выпуска машины
    car_color = models.CharField(max_length=255, verbose_name="Car color")
    number_of_doors = models.PositiveIntegerField(
        default=2, blank=True, verbose_name="Number of doors in car"
    )
    body_type = models.CharField(
        max_length=255, verbose_name="Car body type"
    )  # Тип кузова
    type_drive = models.CharField(
        max_length=255, verbose_name="Car type drive"
    )  # Тип привода
    country = CountryField(countries=G8Countries, verbose_name="Car country")
    volume_fuel_tank = models.PositiveIntegerField(
        blank=False, verbose_name="Car volume of fuel tank"
    )  # Объем топливного бака

    class Meta:
        db_table = "car"
        verbose_name = "Car"


class DealerCars(BaseModel):  # Машины поставщика с ценами
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_cars",
        verbose_name="Dealer of car",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_dealers",
        verbose_name="Car to sale",
    )
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price from dealer",
    )

    class Meta:
        db_table = "dealer_cars"
        verbose_name = "DealerCars"


class DealersSalesHistory(BaseModel):  # История продаж для поставщика / список машин для автосалона
    id_dealer_car = models.ForeignKey(
        DealerCars,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sales_history",
        verbose_name="Dealer and car",
    )  # ссылка на DealerCars, которая содержит и поставщика и машину
    car_dealership = models.ForeignKey(
        "CarDealership.CarDealership",
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_cars",
        verbose_name="Car dealership who bought car",
    )
    discount = models.ForeignKey(
        "CarDealership.Discount",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Discount for bought",
    )
    finally_cost = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price for car dealership",
    )  # цена покупки для автосалона

    class Meta:
        db_table = "dealers_history"
        verbose_name = "DealersSalesHistory"
