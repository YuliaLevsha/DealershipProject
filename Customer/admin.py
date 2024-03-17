from django.contrib import admin
from Customer.models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "balance")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("interested_in_car", "max_price", "customer")


@admin.register(CustomerPurchaseHistory)
class CustomerPurchaseHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ("customer", "id_dealership_car", "cost")
