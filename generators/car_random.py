import random
from base_model import G8Countries


class CarRandom:
    """Класс для генерации полей машины"""
    def __init__(self) -> None:
        self.car_color = ['yellow', 'black', 'white', 'red', 'blue', 'grey', 'green', 'brown']
        self.body_type = ['sedan', 'hatchback', 'SUV(crossover)', 'coupe', 'minivan', 'pickup', 'convertible']
        self.type_drive = ['front', 'rear', 'all']
    
    def random_car_model(self):
        return random.randint(1, 10)
    
    def random_car_year(self):
        return random.randint(1990, 2020)
    
    def random_car_color(self):
        return random.choice(self.car_color)
    
    def random_car_number_of_doors(self):
        return random.randint(2, 5)
    
    def random_car_body_type(self):
        return random.choice(self.body_type)
    
    def random_car_type_drive(self):
        return random.choice(self.type_drive)
    
    def random_car_country(self):
        return random.choice(G8Countries.only)
    
    def random_car_volume_fuel_tank(self):
        return random.randint(40, 80)


car_random = CarRandom()
