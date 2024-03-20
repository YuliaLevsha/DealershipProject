from django.contrib import admin
from Dealer.models import *


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "foundation_year", "customers_count")
    list_filter = ("foundation_year", "customers_count")
    search_fields = ("name",)
    list_display_links = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("car_model", "car_year", "country")
    list_filter = (
        "car_model__name",
        "country",
        "car_year",
        "car_color",
        "body_type",
        "type_drive",
    )
    search_fields = ("car_year", "car_model__name")
    list_display_links = ("car_model",)


@admin.register(DealerCars)
class DealerCarsAdmin(admin.ModelAdmin):
    list_display = ("dealer", "car", "price")
    list_filter = ("dealer__name", "car__car_model__name")
    search_fields = ("dealer__name",)
    list_display_links = ("dealer",)


@admin.register(DealersSalesHistory)
class DealersSalesHistoryAdmin(admin.ModelAdmin):
    list_display = ("id_dealer_car", "car_dealership", "discount", "finally_cost")
    list_filter = ("car_dealership__name", "id_dealer_car__dealer__name")
    search_fields = ("car_dealership__name", "id_dealer_car__dealer__name")
    list_display_links = None
