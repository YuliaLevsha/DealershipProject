from django.db import models
from base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField


class Customer(AbstractUser):
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Customer balance",
    )
    date_birth = models.DateField(blank=False, verbose_name="Customer date birth")
    passport = models.CharField(max_length=10, verbose_name="Customer passport")
    cars = models.ManyToManyField(
        "CarDealership.CarDealershipDealersCar",
        through="CustomerCarDealership",
        verbose_name="List cars of customer",
    )

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"


class Offer(BaseModel):
    max_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Max price of car to buy",
    )
    description_cars = models.JSONField(
        encoder=None, decoder=None, verbose_name="Description future cars to buy"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Customer who create offer",
        related_name="offers",
    )

    class Meta:
        db_table = "offer"
        verbose_name = "Offer"


class CustomerCarDealership(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Customer who buy car",
        related_name="list_cars",
    )
    car = models.ForeignKey(
        "CarDealership.CarDealershipDealersCar",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Car which was bought",
        related_name="customers",
    )
    new_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price for customer",
    )

    class Meta:
        db_table = "customer_car_dealership"
        verbose_name = "CustomerCarDealership"
