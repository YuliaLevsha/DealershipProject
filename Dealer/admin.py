from django.contrib import admin
from Dealer.models import *


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "foundation_year", "customers_count")


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("car_model", "car_year", "country")


@admin.register(DealerCars)
class DealerCarsAdmin(admin.ModelAdmin):
    list_display = ("dealer", "car", "price")


@admin.register(DealersSalesHistory)
class DealersSalesHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ("id_dealer_car", "car_dealership", "discount", "finally_cost")
