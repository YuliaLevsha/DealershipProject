from django.db import models
from base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from rest_framework_simplejwt.tokens import RefreshToken


class Customer(AbstractUser):  # Покупатель (пользователь)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Customer balance",
        default=None,
        null=True
    )  # Баланс
    date_birth = models.DateField(default=None, null=True, blank=False, verbose_name="Customer date birth")
    passport = models.CharField(
        default=None, null=True, max_length=10, verbose_name="Customer passport"
    )  # Серия и номер паспорта

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"


class Offer(BaseModel):  # Оффер, который создает пользователь
    max_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Max price of car to buy",
    )
    interested_in_car = models.ForeignKey(
        "Dealer.Car",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Car which customer wanna buy",
        related_name="customers",
    )  # Машина, которой заинтересован пользователь
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


class CustomerPurchaseHistory(
    BaseModel
):  # История покупок пользователя / история продаж для автосалона
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Customer who buy car",
        related_name="list_cars",
    )
    id_dealership_car = models.ForeignKey(
        "Dealer.DealersSalesHistory",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Car which was bought",
        related_name="customers",
    )  # Какая машины была куплена и в каком салоне
    cost = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Car price for customer",
    )  # За какую цену купил машину пользователь

    class Meta:
        db_table = "customer_history"
        verbose_name = "CustomerPurchaseHistory"
