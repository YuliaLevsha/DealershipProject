from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from djmoney.models.fields import MoneyField
from base_model import BaseModel, G8Countries


class CarDealership(BaseModel):  # Автосалон
    name = models.CharField(max_length=255, verbose_name="Car dealership name")
    location = CountryField(
        countries=G8Countries, verbose_name="Car dealership country"
    )  # Местоположение автосалона
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car dealership balance",
    )  # Баланс
    description_cars = models.JSONField(
        encoder=None, decoder=None, verbose_name="Description future cars to sale"
    )  # Характеристики авто, которые салон будет продавать
    car_models = models.ManyToManyField(
        "Dealer.CarModel",
        through="AvailableCarModels",
        verbose_name="Models to sale",
        related_name="in_dealership",
    )  # Модели авто, которые будут найдены по description_cars
    profitable_dealers = models.ManyToManyField(
        "Dealer.Dealer", through="ProfitableDealers", verbose_name="Profitable dealers"
    )  # Выгодный поставщик, у которых покупаем, и модели какие покупаем
    dealership_cars = models.ManyToManyField(  # Список машин, которые продает автосалон
        "Dealer.DealerCars",
        through="Dealer.DealersSalesHistory",
        verbose_name="Dealership cars to sale",
        related_name="dealerships",
    )

    class Meta:
        db_table = "car_dealership"
        verbose_name = "CarDealership"


class ProfitableDealers(
    BaseModel
):  # Выгодные поставщи, у которых покупаем и модели машин (товар)
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="profit_dealers",
    )
    dealer = models.ForeignKey(
        "Dealer.Dealer",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profitable dealers",
    )
    car_model = models.ForeignKey(
        "Dealer.CarModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profitable car models",
    )

    class Meta:
        db_table = "profitable_dealers"
        verbose_name = "ProfitableDealers"


class Discount(BaseModel):  # Скидка
    start_date = models.DateTimeField(verbose_name="Start discount")  # С какого числа
    finish_date = models.DateTimeField(
        verbose_name="Finish discount"
    )  # По какое число действует
    percent = models.PositiveIntegerField(
        validators=[MaxValueValidator(50)], verbose_name="Percent discount"
    )  # Сколько в % скидка
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_discounts",
        verbose_name="Discount for car dealership",
    )  # На какой салон распространяется скидка
    name = models.CharField(max_length=255, verbose_name="Discount name")
    description = models.CharField(max_length=255, verbose_name="Discount description")
    cars = models.ManyToManyField(
        "Dealer.Car", through="CarsDiscount", verbose_name="Discount for cars"
    )  # Список машин, на которые распространяется акция

    class Meta:
        db_table = "discounts"
        verbose_name = "Discounts"


class CarsDiscount(BaseModel):  # Машины, на которые распространяется акция
    car = models.ForeignKey(
        "Dealer.Car",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Discount available for cars",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_cars",
        verbose_name="Discount",
    )

    class Meta:
        db_table = "cars_discount"
        verbose_name = "CarsDiscount"


class AvailableCarModels(BaseModel):  # Модели машин, который продаются в салоне
    car_model = models.ForeignKey(
        "Dealer.CarModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Model of car",
    )  # Модель машины
    car_dealership = models.ForeignKey(
        CarDealership,
        on_delete=models.SET_NULL,
        null=True,
        related_name="list_car_model",
        verbose_name="Car dealership",
    )  # Автосалон

    class Meta:
        db_table = "available_car_models"
        verbose_name = "AvailableCarModels"
