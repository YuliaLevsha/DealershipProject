import random
import string
from Customer.models import Customer, Offer
from Dealer.models import Dealer, Car, DealerCars, CarModel
from CarDealership.models import CarDealership, AvailableCarModels, Discount
from base_model import G8Countries
from generators.car_random import car_random


EMAILS = ["@mail.ru", "@gmail.com"]


class Generator:
    """Класс создает сущности такие как пользователи, машины, салоны и др.
    Для дальнейше работы селери и проверки"""

    def __init__(self) -> None:
        self.max_length = 12
        self.letters = string.ascii_letters

    def generate_string(self) -> str:
        return "".join(random.choices(self.letters, k=self.max_length))

    def create_customer(self) -> None:
        counts = Customer.objects.all().count()
        future_customer = Customer.objects.create(
            username=self.generate_string(),
            email=f"email_{counts+1}{random.choice(EMAILS)}",
            is_active=True,
            balance=random.randint(50000, 150000),
        )
        future_customer.set_password(future_customer.username + str(future_customer.pk))
        future_customer.save()

    def create_car(self) -> None:
        Car.objects.create(
            car_model=CarModel.objects.get(pk=car_random.random_car_model()),
            car_year=car_random.random_car_year(),
            car_color=car_random.random_car_color(),
            number_of_doors=car_random.random_car_number_of_doors(),
            body_type=car_random.random_car_body_type(),
            type_drive=car_random.random_car_type_drive(),
            country=car_random.random_car_country(),
            volume_fuel_tank=car_random.random_car_volume_fuel_tank(),
        )

    def generate_dealer_cars(self) -> None:
        dealer_count = Dealer.objects.all().count()
        car_indexes = Car.objects.filter(is_active=True).values_list("id", flat=True)
        choice_car = random.choice(car_indexes)
        car = Car.objects.get(pk=choice_car)
        DealerCars.objects.create(
            dealer=Dealer.objects.get(pk=random.randint(1, dealer_count + 1)),
            car=car,
            price=random.randint(20000, 50000),
        )
        car.is_active = False
        car.save()

    def create_dealer(self) -> None:
        Dealer.objects.create(
            name=self.generate_string(), foundation_year=random.randint(2000, 2024)
        )

    def create_dealership(self) -> None:
        car_model = CarModel.objects.get(pk=car_random.random_car_model())
        cardealership = CarDealership.objects.create(
            name=self.generate_string(),
            location=random.choice(G8Countries.only),
            balance=random.randint(100000, 300000),
            description_cars={
                "car_model": car_model.name,
                "car_year": car_random.random_car_year(),
                "car_color": car_random.random_car_color(),
                "number_of_doors": car_random.random_car_number_of_doors(),
                "body_type": car_random.random_car_body_type(),
                "type_drive": car_random.random_car_type_drive(),
                "country": car_random.random_car_country(),
                "volume_fuel_tank": car_random.random_car_volume_fuel_tank(),
            },
        )
        AvailableCarModels.objects.create(
            car_model=car_model, car_dealership=cardealership
        )

    def create_offer(self) -> None:
        car_counts = Car.objects.all().count()
        customer_indexes = Customer.objects.filter(is_active=True).values_list(
            "id", flat=True
        )
        Offer.objects.create(
            max_price=random.randint(10000, 50000),
            customer=Customer.objects.get(
                pk=random.randint(1, random.choice(customer_indexes))
            ),
            interested_in_car=Car.objects.get(pk=random.randint(1, car_counts)),
        )


generator = Generator()
