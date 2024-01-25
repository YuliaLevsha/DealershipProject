from django.db import models
from django_countries.fields import CountryField
from base_model import BaseModel, G8Countries
from django.core.validators import MaxValueValidator
from djmoney.models.fields import MoneyField


class Dealer(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Dealer name')
    foundation_year = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(2024)],
                                                  verbose_name='Dealer foundation year')
    customers_count = models.PositiveIntegerField(default=0, verbose_name='Dealer customers count')
    dealer_cars = models.ManyToManyField('Car', through='DealerCars', verbose_name='Dealers cars to sale',
                                         related_name='dealers')

    class Meta:
        db_table = 'dealer'
        verbose_name = 'Dealer'


class CarModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Name model')

    class Meta:
        db_table = 'car_model'
        verbose_name = 'CarModel'


class Car(BaseModel):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Car model',
                                  related_name='cars')
    car_year = models.PositiveIntegerField(blank=False, verbose_name='Car year')
    car_color = models.CharField(max_length=255, verbose_name='Car color')
    number_of_doors = models.PositiveIntegerField(default=2, blank=True, verbose_name='Number of doors in car')
    body_type = models.CharField(max_length=255, verbose_name='Car body type')
    type_drive = models.CharField(max_length=255, verbose_name='Car type drive')
    country = CountryField(countries=G8Countries, verbose_name='Car country')
    volume_fuel_tank = models.PositiveIntegerField(blank=False, verbose_name='Car volume of fuel tank')

    class Meta:
        db_table = 'car'
        verbose_name = 'Car'


class DealerCars(BaseModel):
    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, related_name='list_cars',
                               verbose_name='Dealer of car')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, related_name='list_dealers',
                            verbose_name='Car to sale')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', verbose_name='Car price from dealer')

    class Meta:
        db_table = 'dealer_cars'
        verbose_name = 'DealerCars'
