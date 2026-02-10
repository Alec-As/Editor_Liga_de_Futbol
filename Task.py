from Time import *
from Resource import *

class Task:
    def __init__(self, task_type: str, name: str, date: Time):
        self.task_type = task_type 
        self.name = name
        self.date = date
        self.resources: list[(str, int)] = []  # Lista de (resource_name, quantity)

    def add_resource(self, resources_input: list[(str, int)]):
        self.resources = resources_input

    def __str__(self):
        return f"{self.task_type.upper()}: {self.name} - {self.date}"

class Match(Task):
    def __init__(self, name: str, date: Time, team1_id: int, team2_id: int, stadium_id: int):
        super().__init__("partido", name, date)
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.stadium_id = stadium_id
        self.local_team_id = team1_id

    def get_principal_team(self): return self.team1_id

    def __str__(self):
        return f"PARTIDO: {self.name}\n" \
                f"Equipos: {self.team1_id} vs {self.team2_id}\n" \
                f"Estadio: {self.stadium_id}"

class Travel(Task):
    def __init__(self, name: str, date: Time, team_id: int, from_stadium_id: int, to_stadium_id: int, distance_km: float):
        super().__init__("viaje", name, date)
        self.team_id = team_id
        self.from_stadium_id = from_stadium_id
        self.to_stadium_id = to_stadium_id
        self.distance_km = distance_km

    def get_principal_team(self): return self.team_id

    def __str__(self):
        return f"VIAJE: {self.name}\n" \
                f"Equipo: {self.team_id}\n" \
                f"De: {self.from_stadium_id} a {self.to_stadium_id}\n" \
                f"Distancia: {self.distance_km}km\n"