from django.contrib import admin
from CarDealership.models import *


@admin.register(CarDealership)
class CarDealershipAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "balance")
    list_filter = ("car_models", "location")
    search_fields = ("name",)
    list_display_links = ("name", )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "start_date",
        "finish_date",
        "percent",
        "car_dealership",
    )
    list_filter = ("car_dealership__name", "percent")
    search_fields = ("percent", "car_dealership__name")
    list_display_links = ('car_dealership', )


@admin.register(AvailableCarModels)
class AvailableCarModelsAdmin(admin.ModelAdmin):
    list_display = ("car_model", "car_dealership")
    list_filter = ("car_model__name", "car_dealership__name")
    search_fields = ("car_model__name", "car_dealership__name")
    list_display_links = ('car_model', )
