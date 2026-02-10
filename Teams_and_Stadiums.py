from Time import *

class Team:
    def __init__(self, name: str, id_num: int, home_stadium_id: int):
        self.name = name
        self.id = id_num
        self.home_stadium_id = home_stadium_id

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Stadium:
    def __init__(self, name: str, id_num: int, max_teams: int):
        self.name = name
        self.id = id_num
        self.max_teams = max_teams
        self.required_resources: list[(str,int)] = []  # Lista de nombres de recursos requeridos

    def _add_resource(self, name: str, quantity: int):
        self.required_resources.append((name, quantity))

    def __str__(self):
        return f"{self.name} (ID: {self.id}, Capacidad: {self.max_teams})"