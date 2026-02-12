import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from Manager import manager
from Time import *

class ApplicationManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Liga de Fútbol")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.create_interface()
        
    def create_interface(self):
        # Frame de botones izquierdo
        self.frame_buttons = tk.Frame(self.root, bg='#2c3e50', width=220)
        self.frame_buttons.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.frame_buttons.grid_propagate(False)
        
        title_buttons = tk.Label(
            self.frame_buttons, 
            text="Gestión de Liga", 
            font=('Arial', 16, 'bold'),
            bg='#34495e',
            fg='white',
            pady=15
        )
        title_buttons.pack(fill='x', pady=(0, 20))
        
        # Botones principales
        buttons = [
            ("🏟️Información", self.show_welcome),
            ("📋Listar Tareas", self.list_all_task),
            ("➕Agregar Partido", self.add_match),
            ("🚌Agregar Viaje", self.add_travel),
            ("🗑️Eliminar Tarea", self.delete_task),
            ("🔍Ver Detalles", self.see_details),
            ("💾Guardar", self.save_state),
            ("📂Cargar", self.load_state)
        ]
        
        for text_aux, command_aux in buttons:
            button = tk.Button(
                self.frame_buttons,
                text=text_aux,
                font=('Arial', 12),
                bg='#3498db',
                fg='white',
                activebackground='#2980b9',
                activeforeground='white',
                relief='flat',
                padx=15,
                pady=10,
                cursor='hand2',
                command=command_aux
            )
            button.pack(fill='x', pady=5, padx=10)
        
        # Frame de información derecha
        self.frame_info = tk.Frame(self.root, bg='white')
        self.frame_info.grid(row=0, column=1, sticky='nsew', padx=(0, 5), pady=5)
        self.frame_info.columnconfigure(0, weight=1)
        self.frame_info.rowconfigure(1, weight=1)
        
        titulo_info = tk.Label(
            self.frame_info, 
            text="Información del Sistema", 
            font=('Arial', 16, 'bold'),
            bg='#1abc9c',
            fg='white',
            pady=12
        )
        titulo_info.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        # Área de texto con scroll
        self.texto_info = scrolledtext.ScrolledText(
            self.frame_info,
            font=('Consolas', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.texto_info.grid(row=1, column=0, sticky='nsew')
        
        # Footer
        footer = tk.Label(
            self.frame_info,
            text="Gestor de Liga de Fútbol v2.0 | 10 Equipos | 10 Estadios",
            font=('Arial', 9),
            bg='#34495e',
            fg='white',
            pady=8
        )
        footer.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        
        self.show_welcome()
    
    def show_welcome(self):
        contenido = """╔═══════════════════════════════════════════════════╗
║       GESTOR DE LIGA DE FÚTBOL - BIENVENIDO       ║
╚═══════════════════════════════════════════════════╝

Este sistema permite gestionar una liga de fútbol con:

• 10 EQUIPOS
• 10 ESTADIOS
• 2 TIPOS DE TAREAS:
    1. PARTIDOS (entre dos equipos en un estadio)
    2. VIAJES (traslado de equipos entre estadios)

Se deben cumplir además los siguientes requisitos para registrar cualquier tarea en el sistema:

• EXISTEN SUFICIENTES RECURSOS EL DÍA ESPECIFICADO PARA LA TAREA ESPECIFICADA:
    1. Los partidos consumen los recursos solicitados por los estadios, los estadios tienen un conjunto de recursos por defecto
    2. Los viajes consumen vehículos en función de la distancia entre estadios(estadio actual -> estadio de llegada)
    3. Los recursos se asignan de forma inteligente y se liberan en cualquier otro día
• CUMPLIMIENTO DEL PLAN DE DESCANSOS:
    1. Después de cada partido los equipos tienen derecho a un descanso de 3 días sin partidos y 1 día sin viajes
    2. Después de cada viaje los equipos tienen derecho a un descanso de 1 día sin partidos y 1 día sin viajes
• CAPACIDAD DE ALOJAMIENTO DE LOS ESTADIOS:
    1. Los estadios tienen por defecto una capacidad máxima de equipos que en un mismo momento puden encontarse alojados
• CUMPLIMIENTO DE LAS REGLAS DE LA LIGA:
    1. Solo dos equipos alojados al mismo tiempo en un mismo estadio pueden jugar un partido
    2. El equipo local debe ser aquel que juege en estadio propio
    3. Dos equipos solo pueden jugar dos veces, y al menos una vez cada equipo de haber jugado de local

─────────────────────────────────────────────────────
➕ RECURSOS DISPONIBLES:
─────────────────────────────────────────────────────"""
        
        for i, resource in enumerate(manager.resources):
            contenido += f"\n{i}. {resource.__str__()}"
        
        contenido += """

─────────────────────────────────────────────────────
🏆 EQUIPOS DISPONIBLES:
─────────────────────────────────────────────────────"""
        
        for i, team in enumerate(manager.teams):
            contenido += f"\n{i}. {team.name} - Estadio Local: {manager.stadiums[team.home_stadium_id].name}"
        
        contenido += """

─────────────────────────────────────────────────────
🏟️ ESTADIOS DISPONIBLES:
─────────────────────────────────────────────────────"""
        
        for i, stadium in enumerate(manager.stadiums):
            contenido += f"\n{i}. {stadium.name} - Capacidad: {stadium.max_teams} equipos - Recursos requeridos: \n"
            for resource_name, quantity in manager.stadiums[i].required_resources:
                contenido += f"{resource_name}({quantity}) "
            contenido += "\n"
        
        contenido += """

─────────────────────────────────────────────────────
📋 INSTRUCCIONES:
─────────────────────────────────────────────────────
1. Use 'Listar Tareas' para ver todas las tareas planificadas
2. Use 'Agregar Partido' para programar un nuevo partido
3. Use 'Agregar Viaje' para planificar el traslado de un equipo
4. Use 'Información' para ver de nuevo este mensaje

Seleccione una opción del menú lateral para comenzar."""
        
        self.update_text(contenido)
    
    def update_text(self, contenido: str):
        self.texto_info.configure(state='normal')
        self.texto_info.delete('1.0', tk.END)
        self.texto_info.insert('1.0', contenido)
        self.texto_info.configure(state='disable')
    
    def list_all_task(self):
        todas_tareas = manager.list_all_tasks()
        
        if not todas_tareas:
            contenido = "📭 NO HAY TAREAS PLANIFICADAS\n\nUse 'Agregar Partido' o 'Agregar Viaje' para crear nuevas tareas."
            self.update_text(contenido)
            return
        
        contenido = "📋 LISTADO COMPLETO DE TAREAS:\n\n"
        contenido += "═" * 60 + "\n\n"
        
        for i, tarea in enumerate(todas_tareas):
            contenido += f"〔{i+1}〕 {manager.task_to_str(tarea)}\n"
            contenido += "─" * 40 + "\n"
        
        contenido += f"\n📊 TOTAL: {len(todas_tareas)} tareas planificadas"
        
        self.update_text(contenido)
        messagebox.showinfo("Listar", f"Se encontraron {len(todas_tareas)} tareas")
    
    def add_match(self):
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Partido")
        dialog.geometry("350x300")
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Título
        tk.Label(dialog, text="⚽ PROGRAMAR NUEVO PARTIDO", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=10)
        
        # Frame para inputs
        input_frame = tk.Frame(dialog, bg='#ecf0f1')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Selección de equipo 1
        tk.Label(input_frame, text="Equipo Local:", bg='#ecf0f1', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        equipo1_var = tk.StringVar()
        equipo1_combo = ttk.Combobox(input_frame, textvariable=equipo1_var, 
                                    values=[f"{i}. {t.name}" for i, t in enumerate(manager.teams)])
        equipo1_combo.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
        # Selección de equipo 2
        tk.Label(input_frame, text="Equipo Visitante:", bg='#ecf0f1', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        equipo2_var = tk.StringVar()
        equipo2_combo = ttk.Combobox(input_frame, textvariable=equipo2_var, 
                                    values=[f"{i}. {t.name}" for i, t in enumerate(manager.teams)])
        equipo2_combo.grid(row=1, column=1, pady=5, padx=10, sticky='ew')
        
        # Fecha
        tk.Label(input_frame, text="Día:", bg='#ecf0f1', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        dia_var = tk.StringVar(value="1")
        dia_spin = tk.Spinbox(input_frame, from_=1, to=31, textvariable=dia_var, width=10)
        dia_spin.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        
        tk.Label(input_frame, text="Mes:", bg='#ecf0f1', font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        mes_var = tk.StringVar(value="1")
        mes_spin = tk.Spinbox(input_frame, from_=1, to=12, textvariable=mes_var, width=10)
        mes_spin.grid(row=3, column=1, pady=5, padx=10, sticky='w')
        
        # Botones
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)
        
        def create_match():
            try:
                # Obtener valores
                equipo1_id = int(equipo1_combo.get().split('.')[0])
                equipo2_id = int(equipo2_combo.get().split('.')[0])
                dia = int(dia_var.get())
                mes = int(mes_var.get())
                
                fecha = Time(dia, mes)
                
                # Crear partido
                resultado = manager.create_match(equipo1_id, equipo2_id, fecha)
                
                if resultado["success"]:
                    messagebox.showinfo("Éxito", resultado["message"])
                    self.list_all_task()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", resultado["message"])
                    
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Por favor complete todos los campos correctamente")
        
        tk.Button(button_frame, text="Crear Partido", command=create_match,
                    bg='#2ecc71', fg='white', font=('Arial', 12), padx=20, pady=5).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="Cancelar", command=dialog.destroy,
                    bg='#e74c3c', fg='white', font=('Arial', 12), padx=20, pady=5).pack(side='left', padx=10)
    
    def add_travel(self):
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Viaje")
        dialog.geometry("350x300")
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Título
        tk.Label(dialog, text="🚌 PROGRAMAR NUEVO VIAJE", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(pady=10)
        
        # Frame para inputs
        input_frame = tk.Frame(dialog, bg='#ecf0f1')
        input_frame.pack(pady=10, padx=20, fill='x')

        # Selección de equipo
        tk.Label(input_frame, text="Equipo:", bg='#ecf0f1', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        equipo_var = tk.StringVar()
        equipo_combo = ttk.Combobox(input_frame, textvariable=equipo_var, 
                                    values=[f"{i}. {t.name}" for i, t in enumerate(manager.teams)])
        equipo_combo.grid(row=0, column=1, pady=5, padx=10, sticky='ew')

        # Selección de estadio
        tk.Label(input_frame, text="Estadio(destino):", bg='#ecf0f1', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        stadium_var = tk.StringVar()
        stadium_combo = ttk.Combobox(input_frame, textvariable=stadium_var, 
                                    values=[f"{i}. {s.name}" for i, s in enumerate(manager.stadiums)])
        stadium_combo.grid(row=1, column=1, pady=5, padx=10, sticky='ew')

        # Fecha
        tk.Label(input_frame, text="Día:", bg='#ecf0f1', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        dia_var = tk.StringVar(value="1")
        dia_spin = tk.Spinbox(input_frame, from_=1, to=31, textvariable=dia_var, width=10)
        dia_spin.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        
        tk.Label(input_frame, text="Mes:", bg='#ecf0f1', font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        mes_var = tk.StringVar(value="1")
        mes_spin = tk.Spinbox(input_frame, from_=1, to=12, textvariable=mes_var, width=10)
        mes_spin.grid(row=3, column=1, pady=5, padx=10, sticky='w')
        
        # Botones
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)

        def create_travel():
            try:
                # Obtener valores
                equipo_id = int(equipo_combo.get().split('.')[0])
                stadium_id = int(stadium_combo.get().split('.')[0])
                dia = int(dia_var.get())
                mes = int(mes_var.get())
                
                fecha = Time(dia, mes)
                
                # Crear partido
                result = manager.create_travel(equipo_id, stadium_id, fecha)
                
                if result["success"]:
                    messagebox.showinfo("Éxito", result["message"])
                    self.list_all_task()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", result["message"])
                    
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Por favor complete todos los campos correctamente")
        
        tk.Button(button_frame, text="Crear Viaje", command=create_travel,
                    bg='#2ecc71', fg='white', font=('Arial', 12), padx=20, pady=5).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="Cancelar", command=dialog.destroy,
                    bg='#e74c3c', fg='white', font=('Arial', 12), padx=20, pady=5).pack(side='left', padx=10)
    
    def delete_task(self):
        all_tasks = manager.list_all_tasks()
        
        if not all_tasks:
            messagebox.showinfo("Eliminar", "No hay tareas para eliminar")
            return
        
        # Crear diálogo para selección
        dialog = tk.Toplevel(self.root)
        dialog.title("Eliminar Tarea")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Seleccione la tarea a eliminar:", 
                font=('Arial', 12)).pack(pady=10)
        
        lista_frame = tk.Frame(dialog)
        lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')
        
        task_list = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, 
                                    font=('Consolas', 10), height=15)
        
        for i, tarea in enumerate(all_tasks):
            task_list.insert(tk.END, f"{i}. {tarea}")
        
        task_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=task_list.yview)
        
        def delete_select():
            selection_index = task_list.curselection()
            if selection_index:
                index = selection_index[0]

                result = manager.delete_task(index)

                if result["success"]:
                    messagebox.showinfo("Éxito", result["message"])
                    self.list_all_task()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", result["message"])
            else:
                messagebox.showwarning("Advertencia", "Seleccione una tarea primero")
        
        tk.Button(dialog, text="Eliminar Seleccionada", command=delete_select,
                    bg='#e74c3c', fg='white', font=('Arial', 12)).pack(pady=10)
        tk.Button(dialog, text="Cancelar", command=dialog.destroy).pack(pady=5)
    
    def see_details(self):
        todas_tareas = manager.list_all_tasks()
        
        if not todas_tareas:
            messagebox.showinfo("Detalles", "No hay tareas para mostrar")
            return
        
        try:
            index = simpledialog.askinteger("Ver Detalles", 
                                            "Índice de la tarea (ver en listado):", 
                                            minvalue=0, maxvalue=len(todas_tareas)-1)
            
            if index is not None:
                tarea = todas_tareas[index]
                
                detalles = f"🔍 DETALLES COMPLETOS DE LA TAREA:\n\n"
                detalles += f"Tipo: {tarea.task_type.upper()}\n"
                detalles += f"Nombre: {tarea.name}\n"
                detalles += f"Fecha: {tarea.date}\n"
                detalles += f"Recursos: {tarea.resources}\n\n"
                
                if hasattr(tarea, 'team1_id'):
                    detalles += f"Equipo Local: {manager.teams[tarea.team1_id].name}\n"
                    detalles += f"Equipo Visitante: {manager.teams[tarea.team2_id].name}\n"
                    detalles += f"Estadio: {manager.stadiums[tarea.stadium_id].name}\n"
                else:
                    detalles += f"Equipo: {manager.teams[tarea.team_id].name}\n"
                    detalles += f"Origen: {manager.stadiums[tarea.from_stadium_id].name}\n"
                    detalles += f"Destino: {manager.stadiums[tarea.to_stadium_id].name}\n"
                    detalles += f"Distancia: {tarea.distance_km} km\n"
                
                self.update_text(detalles)
        except ValueError:
            messagebox.showerror("Error", "Índice inválido")
    
    def save_state(self):
        manager.save_state()
        messagebox.showinfo("Guardar", "Estado guardado exitosamente en 'league_state.json'")
    
    def load_state(self):
        if manager.load_state():
            messagebox.showinfo("Cargar", "Estado cargado exitosamente")
            self.show_welcome()
        else:
            messagebox.showwarning("Cargar", "No se encontró archivo de estado previo")

def main():
    root = tk.Tk()
    app = ApplicationManagement(root)
    root.mainloop()

if __name__ == "__main__":
    main()