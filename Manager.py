import json
from Teams_and_Stadiums import *
from Task import *
from Resource import *
from Time import *

class LeagueManager:
    def __init__(self):

        self.teams = [
            Team("Atlético Capital", 0, 0),
            Team("Centuria FC", 1, 1),
            Team("Monumental Buenos Aires", 2, 2),
            Team("Águilas Aztecas", 3, 3),
            Team("Carioca Stars", 4, 4),
            Team("Nou Catalans", 5, 5),
            Team("Red Warriors", 6, 6),
            Team("Allianz Baviera", 7, 7),
            Team("AC Milano", 8, 8),
            Team("Vikingos Blancos", 9, 9),
        ]

        self.total_teams = len(self.teams)

        self.stadiums = [
            Stadium("Estadio Nacional", 0, 3),
            Stadium("Estadio Centenario", 1, 2),
            Stadium("Estadio Monumental", 2, 4),
            Stadium("Estadio Azteca", 3, 2),
            Stadium("Estadio Maracaná", 4, 3),
            Stadium("Estadio Camp Nou", 5, 2),
            Stadium("Estadio Old Trafford", 6, 3),
            Stadium("Estadio Allianz Arena", 7, 5),
            Stadium("Estadio San Siro", 8, 2),
            Stadium("Estadio Bernabéu", 9, 3),
        ]
        
        self.distance_matrix = [
            [0, 150, 300, 450, 200, 350, 400, 250, 500, 100],
            [150, 0, 200, 350, 100, 250, 300, 150, 400, 50],
            [300, 200, 0, 150, 250, 100, 150, 200, 250, 200],
            [450, 350, 150, 0, 400, 250, 300, 350, 100, 350],
            [200, 100, 250, 400, 0, 150, 200, 50, 300, 150],
            [350, 250, 100, 250, 150, 0, 50, 100, 200, 250],
            [400, 300, 150, 300, 200, 50, 0, 150, 250, 300],
            [250, 150, 200, 350, 50, 100, 150, 0, 400, 200],
            [500, 400, 250, 100, 300, 200, 250, 400, 0, 450],
            [100, 50, 200, 350, 150, 250, 300, 200, 450, 0]
        ]
        
        self.resources: list[Vehicle | Instrument_Personal] = [
            Vehicle("Avión", 1, 500),
            Vehicle("Autobús", 3, 250),
            Vehicle("Van", 5, 100),

            Instrument_Personal("Ambulancia", 1),
            Instrument_Personal("Árbitro", 3),
            Instrument_Personal("Médico", 3),
            Instrument_Personal("Seguridad", 3),
            Instrument_Personal("Cámaras TV", 2),
        ]
        
        self.schedule: dict[str, list[Match | Travel]] = {} #Calendario, clave: fecha en formato str devuelve una lista de todas las tareas asignadas

        self.played_against = [[False] * self.total_teams for _ in range(self.total_teams)] #Matriz para registrar los juegos ya planificados
        
        for stadium in self.stadiums:
            stadium._add_resource("Árbitro", 1)
            stadium._add_resource("Médico", 1)
            stadium._add_resource("Seguridad", 1)
            if stadium.id % 2 == 0:
                stadium._add_resource("Cámaras TV", 1)
            if stadium.id % 3 == 0:
                stadium._add_resource("Ambulancia", 1)

    def _can_play_match(self, date: Time, team_id: int)-> bool:
        if self.schedule:
            copy_date = date.copy()
            copy_date.next_day(-3)

            for _ in range(7):
                if self.schedule.get(copy_date.__str__()):

                    for task in self.schedule[copy_date.__str__()]:
                        if task.task_type == "partido":
                            if task.team1_id == team_id or task.team2_id == team_id: return False
                        
                        if (_ >= -1 and _ <= 1) and task.task_type == "viaje":
                            if task.team_id == team_id : return False

                copy_date.next_day(1)
        return True
    
    def _can_travel(self, date: Time, team_id: int)-> bool:
        if self.schedule:
            copy_date = date.copy()
            copy_date.next_day(-1)

            for _ in range(3):
                if self.schedule.get(copy_date.__str__()):

                    for task in self.schedule[copy_date.__str__()]:
                        if task.task_type == "partido":
                            if task.team1_id == team_id or task.team2_id == team_id: return False

                        if task.task_type == "viaje":
                            if task.team_id == team_id : return False

                copy_date.next_day(1)
        return True
    
    def _can_host_team(self, date: Time, stadium_id: int)-> bool:
        if self.schedule:
            current_teams_count = 1
            state_teams: dict[int, int]= {} #(id, cantidad de días de la última comprobación)

            for task_day_str, tasks in self.schedule.items():
                task_day = self._str_to_time(task_day_str)
                if not self._is_newer_day(date, task_day): continue

                for task in tasks:
                    if task.task_type != "viaje": continue

                    if task.from_stadium_id == stadium_id:
                        if state_teams.get(task.team_id):
                            if state_teams[task.team_id] < self._days_between(date, task_day): continue
                        state_teams[task.team_id] = self._days_between(date, task_day)
                        current_teams_count -= 1


                    if task.to_stadium_id == stadium_id:
                        if state_teams.get(task.team_id):
                            if state_teams[task.team_id] < self._days_between(date, task_day): continue
                        state_teams[task.team_id] = self._days_between(date, task_day)
                        current_teams_count += 1


            return self.stadiums[stadium_id].max_teams >= current_teams_count
        return True
    
    def _can_allot_instrument_personal(self,date: Time, resources_required: list[(str, int)])-> bool:
        if not self.schedule.get(date.__str__()): return True
        current_reserve = {} #Cantidad de objetos actualmente reservados en la fecha solicitada, pendiente de calculo {resource_name: quantity}

        for task in self.schedule[date.__str__()]:
            if task.task_type != "partido": continue

            for i in task.resources:
                resource = i[0]
                quantity = i[1]
                current_reserve[resource] = current_reserve.get(resource, 0) + quantity

        for i in resources_required:
            resource = i[0]
            quantity = i[1]
            total_quantity = self._search_total_quantity_resource(resource)

            if current_reserve.get(resource):
                current_quantity = total_quantity - current_reserve[resource] 
                if current_quantity < quantity: return False

        return True
    
    def _can_allot_vehicle(self, date: Time, distance: int, resources_require: list[(str, int)]) -> bool:
        available_vehicles: list[Vehicle] = []
        for resource in self.resources:
            if resource.type == "vehículo":
                available_vehicles.append(resource)
        available_vehicles.sort(key=lambda v: v.reach)

        current_reserve = {}
        if self.schedule.get(date.__str__()):
            for task in self.schedule[date.__str__()]:
                if task.task_type != "viaje": continue
                for i in task.resources:
                    resource_name = i[0]
                    quantity = i[1]
                    current_reserve[resource_name] = current_reserve.get(resource_name, 0) + quantity
    
        available_counts = {}
        for vehicle in available_vehicles:
            reserved = current_reserve.get(vehicle.name, 0)
            available_counts[vehicle.name] = vehicle.total_quantity - reserved
    
        remaining_distance = distance
        assigned_vehicles = []

        vehicle_types = available_vehicles.copy()
    
        while remaining_distance > 0 and vehicle_types:
            for vehicle in vehicle_types:
                if remaining_distance <= 0: break
                if available_counts[vehicle.name] <= 0: continue
            
                vehicle_range = vehicle.reach
        
                if vehicle_range >= remaining_distance:
                    assigned_vehicles.append((vehicle.name, 1))
                    available_counts[vehicle.name] -= 1
                    remaining_distance = 0
                    break
        
                max_to_use = min(available_counts[vehicle.name], 
                    (remaining_distance + vehicle_range - 1) // vehicle_range)
        
                if max_to_use > 0:
                    assigned_vehicles.append((vehicle.name, max_to_use))
                    remaining_distance -= max_to_use * vehicle_range
                    available_counts[vehicle.name] -= max_to_use
            
                if remaining_distance <= 0: break
                
            if remaining_distance > 0:
                vehicle_types = [v for v in vehicle_types if available_counts[v.name] > 0]
                if not vehicle_types: return False
    
        if remaining_distance > 0: return False
    
        resources_require.clear()
        resources_require.extend(assigned_vehicles)
    
        return True
    
    def _search_current_location_for_team(self, date: Time, team: Team) -> int:
        current_location = team.home_stadium_id
        current_days_diff = 3_650 # diferencia inicial, 10 años

        for task_date_str, tasks in self.schedule.items():
            task_date = self._str_to_time(task_date_str)

            if not self._is_newer_day(date, task_date): continue

            for task in tasks:
                if task.task_type != "viaje": continue
                if task.team_id == team.id:
                    days_diff = self._days_between(task_date, date)
                    if days_diff <= current_days_diff:
                        current_location = task.to_stadium_id
                        current_days_diff = days_diff

        return current_location
    
    def _search_total_quantity_resource(self, name: str)-> int:
        quantity = 0
        for resource in self.resources:
            if resource.name == name:
                quantity = resource.total_quantity
                break
        return quantity

    #Retorna true si la fecha 1 es más vieja o igual que la fecha 2
    def _is_newer_day(self, date1: Time, date2: Time) -> bool:
        if date1.year > date2.year: return True

        elif date1.year == date2.year:
            if date1.month > date2.month: return True

            elif date1.month == date2.month: return date1.day >= date2.day

        return False
    
    def _days_between(self, date1: Time, date2: Time) -> int:
        days_month = []
        for i in range(12):
            days_month.append(date1.days_month(i+1, date1.year))

        day1 = sum(days_month[:date1.month-1]) + date1.day
        day2 = sum(days_month[:date2.month-1]) + date2.day
        return abs(day2 - day1)
    
    def _search_older_tasks(self, date: Time, team_id: int):
        list_older_tasks = []

        for date_task_str, tasks in self.schedule.items():
            date_task = self._str_to_time(date_task_str)
            if self._is_newer_day(date, date_task): continue

            for task in tasks:
                if task.task_type == "partido" and (team_id == task.team1_id or team_id == task.team2_id):
                    list_older_tasks.append(task)

                elif task.task_type == "viaje" and team_id == task.team_id:
                    list_older_tasks.append(task)
        
        return list_older_tasks

    def _save_match(self, date: Time, local_id: int, visitor_id: int, resources: list[(str, int)])-> Match:
        team1 = self.teams[local_id]
        team2 = self.teams[visitor_id]
        match_name = f"{team1.name} vs {team2.name} del {date.__str__()}"

        match = Match(match_name, date, local_id, visitor_id, team1.home_stadium_id)
        match.add_resource(resources)

        if date.__str__() not in self.schedule:
            self.schedule[date.__str__()] = []
        self.schedule[date.__str__()].append(match)
        self.played_against[local_id][visitor_id] = True

        return match

    def _save_travel(self, date: Time, team_id: int, current_stadium_id: int, to_stadium_id: int, distance: float, resources: list[(str, int)])-> Travel:
        team = self.teams[team_id]
        to_stadium = self.stadiums[to_stadium_id]
        travel_name = f"Viaje {team.name} a {to_stadium.name} del {date.__str__()}"

        travel = Travel(travel_name, date, team_id, current_stadium_id, to_stadium_id, distance)
        travel.add_resource(resources)

        if date.__str__() not in self.schedule:
            self.schedule[date.__str__()] = []
        self.schedule[date.__str__()].append(travel)

        return travel
    
    def _str_to_time(self, time_str: str) -> Time:
        day, month, year = map(int, time_str.split('/'))
        return Time(day, month, year)

    def get_distance(self, stadium1_id: int, stadium2_id: int) -> float:
        return self.distance_matrix[stadium1_id][stadium2_id]
    
    def task_to_str(self, task: Match | Travel):
        if task.task_type == "partido":
            return f"PARTIDO: {task.name}\n" \
                f"Equipos: {self.teams[task.team1_id]} vs {self.teams[task.team2_id]}\n" \
                f"Estadio: {self.stadiums[task.stadium_id]}"
        if task.task_type == "viaje":
            return f"VIAJE: {task.name}\n" \
                f"Equipo: {self.teams[task.team_id]}\n" \
                f"De: {self.stadiums[task.from_stadium_id]} a {self.stadiums[task.to_stadium_id]}\n" \
                f"Distancia: {task.distance_km}km\n"
    
    def create_match(self, team1_id: int, team2_id: int, date: Time) -> dict:
        team1 = self.teams[team1_id]
        team2 = self.teams[team2_id]
        stadium = self.stadiums[team1.home_stadium_id]
        
        # 1. Verificar que no sean el mismo equipo
        if team1_id == team2_id:
            return {"success": False, "message": "Un equipo no puede jugar contra sí mismo"}
        
        # 2. Verificar que el equipo 1 este en su estadio para jugar de local
        if stadium.id != self._search_current_location_for_team(date, team1):
            return {"success": False, "message": f"El equipo {team1.name} no se encuentra en su estadio para jugar de local"}
        # 2.5. Verificar que el equipo 2 este en el mismo estadio que el equipo 1
        if stadium.id != self._search_current_location_for_team(date, team2):
            return {"success": False, "message": f"El equipo {team2.name} no se encuentra en el mismo estadio que {team1.name}"}
        
        # 3. Verificar que equipos puedan jugar (3 días entre partidos)
        if not self._can_play_match(date, team1_id):
            return {"success": False, "message": f"El equipo : {team1.name} no puede jugar (mínimo 3 días entre partidos)"}
        if not self._can_play_match(date, team2_id):
            return {"success": False, "message": f"El equipo : {team2.name} no puede jugar (mínimo 3 días entre partidos)"}
        
        # 4. Verificar si el partido ya se ha jugado en la liga
        if self.played_against[team1_id][team2_id]:
            return {"success": False, "message": f"Estos equipos ya tienen un partido planificado en esta liga con el equipo: {team1.name} como local"}
        
        # 5. Verificar recursos requeridos
        if not self._can_allot_instrument_personal(date, stadium.required_resources):
            return {"success": False, "message": f"No hay suficientes recursos disponibles para la fecha:{date.__str__()}"}
        
        match = self._save_match(date, team1_id, team2_id, stadium.required_resources)
        
        return {"success": True, "message": "Partido creado exitosamente", "match": match}
    
    def create_travel(self, team_id: int, to_stadium_id: int, date: Time) -> dict:
        team = self.teams[team_id]
        current_stadium_id = self._search_current_location_for_team(date, team)
        
        # 1. Verificar que no sea el mismo estadio
        if current_stadium_id == to_stadium_id:
            return {"success": False, "message": "El equipo ya está en ese estadio"}
        
        # 2. Verificar que equipo pueda viajar (1 día entre viajes)
        if not self._can_travel(date, team_id):
            return {"success": False, "message": "El equipo no puede viajar (mínimo 1 día entre viajes)"}
        
        # 3. Verificar capacidad del estadio destino
        to_stadium = self.stadiums[to_stadium_id]
        if not self._can_host_team(date, to_stadium_id):
            return {"success": False, "message": f"El estadio {to_stadium.name} no puede alojar más equipos en esta fecha"}
        
        # 4. Calcular distancia y vehículos necesarios
        distance = self.get_distance(current_stadium_id, to_stadium_id)
        resources_requiere: list[(str, int)] = []
        if not self._can_allot_vehicle(date, distance, resources_requiere):
            return {"success": False, "message": f"No hay transportes suficientes para recorrer {distance}km para la fecha: {date.__str__()}"}
        
        #5. Determinar si existen afectaciones al calendario en las tareas ya planificadas
        list_older_tasks = self._search_older_tasks(date, team_id)
        if list_older_tasks:
            return {"success": False, "message"
                    : f"No se puede agregar la tarea en esta fecha porque existen {len(list_older_tasks)} tarea/s planificada/s en fechas posteriores que se ven afectadas"}
        
        travel = self._save_travel(date, team_id, current_stadium_id, to_stadium_id, distance, resources_requiere)
        
        return {"success": True, "message": "Viaje creado exitosamente", "travel": travel}
    
    def list_all_tasks(self):
        all_tasks: list[Match | Travel] = []
        for tasks_list in self.schedule.values():
            all_tasks.extend(tasks_list)

        all_tasks.sort(key=lambda task: (
        task.date.year, 
        task.date.month, 
        task.date.day
        ))
        return all_tasks
    
    def get_task_details(self, index: int):
        all_tasks = self.list_all_tasks()
        if 0 <= index < len(all_tasks):
            return all_tasks[index]
        return None
    
    def delete_task(self, index: int):
        try:
            all_tasks = self.list_all_tasks()

            if 0 <= index < len(all_tasks):
                task_to_delete = all_tasks[index]

                task_team = task_to_delete.get_principal_team()

                task_date = task_to_delete.date.__str__()
                if task_date not in self.schedule: return False
                found = False

                tasks_for_date = self.schedule[task_date]

                for task in tasks_for_date:
                    if task_team == task_to_delete.get_principal_team():
                        tasks_for_date.remove(task)
                        found = True

                        if task.task_type == "partido":
                            self.played_against[task.team1_id][task.team2_id] = False
                        break
                if found and not tasks_for_date:
                    del self.schedule[task_date]
                return found

            return False
        except (IndexError, KeyError, ValueError):
            return False
    
    def save_state(self, filename: str = "league_state.json"):
        state = {
            "teams": [],
            "stadiums": [],
            "schedule": {},
            "resources": [],
            "played_against": self.played_against,
            "distance_matrix": self.distance_matrix
        }
    
        # Guardar equipos 
        for team in self.teams:
            team_state = {
                "id": team.id,
                "name": team.name,
                "home_stadium_id": team.home_stadium_id
            }
            state["teams"].append(team_state)
    
        # Guardar estadios
        for stadium in self.stadiums:
            stadium_state = {
                "id": stadium.id,
                "name": stadium.name,
                "max_teams": stadium.max_teams,
                "required_resources": stadium.required_resources
            }
            state["stadiums"].append(stadium_state)
    
        # Guardar calendario (schedule)
        for date_str, tasks in self.schedule.items():
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "name": task.name,
                    "task_type": task.task_type,
                    "date": {
                        "day": task.date.day,
                        "month": task.date.month,
                        "year": task.date.year
                    },
                    "resources": task.resources
                }
            
                # Agregar atributos específicos según el tipo
                if task.task_type == "partido":
                    task_dict.update({
                        "team1_id": task.team1_id,
                        "team2_id": task.team2_id,
                        "stadium_id": task.stadium_id,
                        "local_team_id": task.local_team_id
                    })
                elif task.task_type == "viaje":
                    task_dict.update({
                        "team_id": task.team_id,
                        "from_stadium_id": task.from_stadium_id,
                        "to_stadium_id": task.to_stadium_id,
                        "distance_km": task.distance_km
                    })
            
            tasks_list.append(task_dict)
        
        state["schedule"][date_str] = tasks_list
    
        # Guardar recursos
        for resource in self.resources:
            resource_dict = {
                "name": resource.name,
                "type": resource.type,
                "total_quantity": resource.total_quantity
                }
        
            # Agregar atributos específicos
            if hasattr(resource, 'reach'):
                resource_dict["reach"] = resource.reach
        
            state["resources"].append(resource_dict)
    
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
        return True

    def load_state(self, filename: str = "league_state.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                state = json.load(f)
        
            # 1. Cargar equipos
            self.teams = []
            for team_data in state["teams"]:
                team = Team(
                    team_data["name"],
                    team_data["id"],
                    team_data["home_stadium_id"]
                )
                self.teams.append(team)
        
            # 2. Cargar estadios
            self.stadiums = []
            for stadium_data in state["stadiums"]:
                stadium = Stadium(
                    stadium_data["name"],
                    stadium_data["id"],
                    stadium_data["max_teams"]
                )
                stadium.required_resources = stadium_data.get("required_resources", [])
                self.stadiums.append(stadium)
        
            # 3. Cargar recursos
            self.resources = []
            for resource_data in state["resources"]:
                if resource_data["type"] == "vehículo":
                    resource = Vehicle(
                        resource_data["name"],
                        resource_data["total_quantity"],
                        resource_data.get("reach", 0)
                    )
                else:  # instrumento_personal
                    resource = Instrument_Personal(
                        resource_data["name"],
                        resource_data["total_quantity"]
                    )
                self.resources.append(resource)
        
            # 4. Cargar calendario (schedule)
            self.schedule = {}
            for date_str, tasks_data in state["schedule"].items():
                tasks_list = []
                for task_data in tasks_data:

                    date_obj = Time(
                        task_data["date"]["day"],
                        task_data["date"]["month"],
                        task_data["date"].get("year", 2024)
                    )
                
                    if task_data["task_type"] == "partido":
                        task = Match(
                            task_data["name"],
                            date_obj,
                            task_data["team1_id"],
                            task_data["team2_id"],
                            task_data["stadium_id"]
                        )
                        task.local_team_id = task_data.get("local_team_id")
                    elif task_data["task_type"] == "viaje":
                        task = Travel(
                            task_data["name"],
                            date_obj,
                            task_data["team_id"],
                            task_data["from_stadium_id"],
                            task_data["to_stadium_id"],
                            task_data["distance_km"]
                        )
                
                    # Asignar recursos
                    task.add_resource(task_data.get("resources", []))
                    tasks_list.append(task)
            
                self.schedule[date_str] = tasks_list
        
            # 5. Cargar otros datos
            self.played_against = state.get("played_against", 
                                       [[False] * self.total_teams for _ in range(self.total_teams)])
            self.distance_matrix = state.get("distance_matrix", self.distance_matrix)
        
            return True
        
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado. Creando nueva liga.")
            return False
        except json.JSONDecodeError:
            print(f"Error al leer {filename}. Formato JSON inválido.")
            return False
        except Exception as e:
            print(f"Error al cargar estado: {e}")
            return False

# Instancia global del manager
manager = LeagueManager()

