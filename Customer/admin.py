from django.contrib import admin
from Customer.models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "balance", 'date_birth')
    list_filter = ('is_active', )
    search_fields = ('username', 'email')
    list_display_links = ('username', )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("interested_in_car", "max_price", "customer")
    list_filter = ('interested_in_car__car_model__name', 'customer__username')
    search_fields = ('customer__username', 'max_price')
    list_display_links = ('interested_in_car', )


@admin.register(CustomerPurchaseHistory)
class CustomerPurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("customer", "id_dealership_car", "cost")
    list_filter = ('customer__username', 'id_dealership_car__id_dealer_car__car__car_model__name')
    search_fields = ('customer__username', 'id_dealership_car')
    list_display_links = None
