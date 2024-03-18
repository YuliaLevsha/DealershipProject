from generators.base_generator import generator
from celery import shared_task
from Dealer.models import DealersSalesHistory, DealerCars
from CarDealership.models import AvailableCarModels, Discount, CarDealership
from Customer.models import Offer, CustomerPurchaseHistory
from django.utils import timezone
import random
from moneyed import Money


def check_discount(dealership: CarDealership) -> None | Discount:
    current_date = timezone.now()
    discounts = Discount.objects.filter(
        car_dealership=dealership,
        start_date__lte=current_date,
        finish_date__gte=current_date,
        is_active=True,
    )
    if len(discounts):
        return Discount.objects.get(
            pk=random.choice(discounts.values_list("id", flat=True))
        )
    else:
        return None


@shared_task
def generate_cars() -> None:
    generator.create_car()
    generator.generate_dealer_cars()


@shared_task
def generate_main_objects() -> None:
    generator.create_customer()
    generator.create_dealer()
    generator.create_dealership()
    generator.create_offer()


@shared_task
def dealership_buy_from_dealer() -> None:
    for car_model_wanna_buy in AvailableCarModels.objects.filter(
        is_active=True
    ).order_by("car_dealership__name"):
        for dealer_this_model in DealerCars.objects.filter(
            is_active=True, car__car_model=car_model_wanna_buy.car_model
        ).order_by("price"):
            discount = check_discount(car_model_wanna_buy.car_dealership)
            new_cost = dealer_this_model.price
            if discount:
                new_cost = Money(
                    dealer_this_model.price * (1 - discount.percent / 100), "USD"
                )
            if car_model_wanna_buy.car_dealership.balance - new_cost >= Money(0, "USD"):
                DealersSalesHistory.objects.create(
                    id_dealer_car=dealer_this_model,
                    car_dealership=car_model_wanna_buy.car_dealership,
                    discount=discount,
                    finally_cost=new_cost,
                )
                car_model_wanna_buy.car_dealership.balance -= new_cost
                car_model_wanna_buy.car_dealership.save()
                dealer_this_model.is_active = False
                dealer_this_model.save()
            else:
                continue


@shared_task
def customer_buy_from_dealership() -> None:
    for offer in (
        Offer.objects.filter(is_active=True)
        .exclude(customer__balance=None)
        .order_by("customer__username")
    ):
        for dealership in DealersSalesHistory.objects.filter(
            id_dealer_car__car=offer.interested_in_car,
            is_active=True,
            finally_cost__lte=offer.max_price,
        ).order_by("finally_cost"):
            new_cost = dealership.finally_cost + Money(random.randint(5, 20), "USD")
            if offer.customer.balance - new_cost >= Money(0, "USD"):
                CustomerPurchaseHistory.objects.create(
                    customer=offer.customer, id_dealership_car=dealership, cost=new_cost
                )
                offer.customer.balance -= new_cost
                offer.customer.save()
                offer.is_active = False
                offer.save()
                dealership.is_active = False
                dealership.save()
            else:
                continue
