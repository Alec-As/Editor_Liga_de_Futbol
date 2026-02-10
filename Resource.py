from Time import *


class Resource:
    def __init__(self, name: str, resource_type: str, total_quantity: int):
        self.name = name
        self.type = resource_type
        self.total_quantity = total_quantity

    def __str__(self):
        return f"{self.name} ({self.type}): {self.total_quantity}"
    
class Instrument_Personal(Resource):
    def __init__(self, name: str, total_quantity: int):
        super().__init__(name, "instrumento_personal", total_quantity)

    def __str__(self):
        return f"{self.name} ({self.type}): {self.total_quantity}"
    
class Vehicle(Resource):
    def __init__(self, name: str, total_quantity: int, reach: int):
        super().__init__(name, "vehículo", total_quantity)
        self.reach = reach

    def __str__(self):
        return f"{self.name} ({self.type}): {self.total_quantity}, {self.reach}"