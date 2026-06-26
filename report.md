# Sistema de Gestión de Liga de Fútbol

**Sistema inteligente de planificación y gestión de partidos y viajes para ligas profesionales.**

---

## 🎯 ¿Qué problema resuelve?

Organizar una liga de fútbol no es solo poner fechas en un calendario. Es un rompecabezas logístico donde cada decisión afecta a todo el sistema. Este proyecto nace de esa necesidad: **automatizar la planificación respetando todas las restricciones** que una liga real impone.

- **Recursos limitados**: Vehículos, árbitros, médicos, seguridad... todo tiene un costo y disponibilidad.
- **Descansos obligatorios**: Los equipos no pueden jugar todos los días.
- **Capacidad de estadios**: No todos los equipos pueden alojarse en el mismo lugar.
- **Reglas de competición**: Cada equipo debe jugar de local al menos una vez, y no pueden repetirse enfrentamientos sin control.

El sistema se encarga de **validar cada solicitud** antes de registrarla, garantizando que el calendario siempre sea consistente y realista.

---

## 🚀 ¿Cómo ejecutarlo?

```bash
# 1. Clonar o descargar el repositorio
git clone [url-del-repositorio]
cd GestorLiga

# 2. Ejecutar (no requiere dependencias externas)
python main.py 
```

## Enfoque General
Este sistema permite gestionar una liga de fútbol con:

- **10 EQUIPOS**
- **10 ESTADIOS**
- **2 TIPOS DE TAREAS**:
    1. **PARTIDOS** (entre dos equipos en un estadio)
    2. **VIAJES** (traslado de equipos entre estadios)

## Requisitos para Registrar Tareas

Para registrar cualquier tarea en el sistema, se deben cumplir los siguientes requisitos:

### 1. Suficiencia de Recursos

- **Partidos**: Consumen los recursos solicitados por los estadios. Los estadios tienen un conjunto de recursos por defecto.
- **Viajes**: Consumen vehículos en función de la distancia entre estadios (estadio actual → estadio de llegada).
- Los recursos se asignan de forma inteligente y se liberan en cualquier otro día.

### 2. Cumplimiento del Plan de Descansos

- Después de cada partido, los equipos tienen derecho a un descanso de:
  - **3 días** sin partidos
  - **1 día** sin viajes
- Después de cada viaje, los equipos tienen derecho a un descanso de:
  - **1 día** sin partidos
  - **1 día** sin viajes

### 3. Capacidad de Alojamiento de los Estadios

- Los estadios tienen por defecto una capacidad máxima de equipos que pueden encontrarse alojados en un mismo momento.

### 4. Cumplimiento de las Reglas de la Liga

- Solo dos equipos alojados al mismo tiempo en un mismo estadio pueden jugar un partido.
- El equipo local debe ser aquel que juegue en su estadio propio.
- Dos equipos solo pueden jugar dos veces, y al menos una vez cada equipo debe haber jugado de local.

---

## ➕ RECURSOS DISPONIBLES

| # | Recurso | Tipo | Cantidad |
|---|---------|------|----------|
| 0 | Avión | vehículo | 1, 500 |
| 1 | Autobús | vehículo | 3, 250 |
| 2 | Van | vehículo | 5, 100 |
| 3 | Ambulancia | instrumento_personal | 1 |
| 4 | Árbitro | instrumento_personal | 3 |
| 5 | Médico | instrumento_personal | 3 |
| 6 | Seguridad | instrumento_personal | 3 |
| 7 | Cámaras TV | instrumento_personal | 2 |

---

## 🏆 EQUIPOS DISPONIBLES

| # | Equipo | Estadio Local |
|---|--------|---------------|
| 0 | Atlético Capital | Estadio Nacional |
| 1 | Centuria FC | Estadio Centenario |
| 2 | Monumental Buenos Aires | Estadio Monumental |
| 3 | Águilas Aztecas | Estadio Azteca |
| 4 | Carioca Stars | Estadio Maracaná |
| 5 | Nou Catalans | Estadio Camp Nou |
| 6 | Red Warriors | Estadio Old Trafford |
| 7 | Allianz Baviera | Estadio Allianz Arena |
| 8 | AC Milano | Estadio San Siro |
| 9 | Vikingos Blancos | Estadio Bernabéu |

---

## 🏟️ ESTADIOS DISPONIBLES

| # | Estadio | Capacidad | Recursos Requeridos |
|---|---------|-----------|---------------------|
| 0 | Estadio Nacional | 3 equipos | Árbitro(1) Médico(1) Seguridad(1) Cámaras TV(1) Ambulancia(1) |
| 1 | Estadio Centenario | 2 equipos | Árbitro(1) Médico(1) Seguridad(1) |
| 2 | Estadio Monumental | 4 equipos | Árbitro(1) Médico(1) Seguridad(1) Cámaras TV(1) |
| 3 | Estadio Azteca | 2 equipos | Árbitro(1) Médico(1) Seguridad(1) Ambulancia(1) |
| 4 | Estadio Maracaná | 3 equipos | Árbitro(1) Médico(1) Seguridad(1) Cámaras TV(1) |
| 5 | Estadio Camp Nou | 2 equipos | Árbitro(1) Médico(1) Seguridad(1) |
| 6 | Estadio Old Trafford | 3 equipos | Árbitro(1) Médico(1) Seguridad(1) Cámaras TV(1) Ambulancia(1) |
| 7 | Estadio Allianz Arena | 5 equipos | Árbitro(1) Médico(1) Seguridad(1) |
| 8 | Estadio San Siro | 2 equipos | Árbitro(1) Médico(1) Seguridad(1) Cámaras TV(1) |
| 9 | Estadio Bernabéu | 3 equipos | Árbitro(1) Médico(1) Seguridad(1) Ambulancia(1) |

---

## 📋 INSTRUCCIONES

1. Use **'Listar Tareas'** para ver todas las tareas planificadas.
2. Use **'Agregar Partido'** para programar un nuevo partido.
3. Use **'Agregar Viaje'** para planificar el traslado de un equipo.
4. Use **'Información'** para ver de nuevo este mensaje.