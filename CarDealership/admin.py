from django.contrib import admin
from CarDealership.models import *


@admin.register(CarDealership)
class CarDealershipAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "balance")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "start_date",
        "finish_date",
        "percent",
        "car_dealership",
    )


@admin.register(AvailableCarModels)
class AvailableCarModelsAdmin(admin.ModelAdmin):
    list_display = ("car_model", "car_dealership")
