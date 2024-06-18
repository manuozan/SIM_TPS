import random
import queue
import json
import tkinter as tk
from tkinter import ttk
import math

# Parámetros de la simulación
NUM_SECTORES = 8
TIEMPO_ENTRE_LLEGADAS = 13  # minutos
DURACION_SIMULACION = 8 * 60 # minutos (1 hora)

# Costos de estacionamiento por tipo de auto
COSTO_POR_HORA = {
    'small': 300,
    'grande': 500,
    'utilitario': 1000
}

# Probabilidades de tipo de auto
PROBABILIDADES_TIPO = {
    'small': 0.45,
    'grande': 0.25,
    'utilitario': 0.30
}

# Probabilidades de tiempo de estacionamiento
PROBABILIDADES_TIEMPO = {
    60: 0.50,
    120: 0.30,
    180: 0.15,
    240: 0.05
}

class Auto:
    _id_counter = 1

    def __init__(self, tipo, tiempo_estacionamiento,estado=None):
        self.id = Auto._id_counter
        Auto._id_counter += 1
        self.tipo = tipo
        self.tiempo_estacionamiento = tiempo_estacionamiento
        self.estado = estado
        self.tiempo_llegada = None
        self.tiempo_salida = None
        self.tiempo_inicio_cobro = None
        self.tiempo_espera_cobro = None

    def __repr__(self):
        return f"Auto {self.id} (Tipo: {self.tipo}, Estado: {self.estado})"

class PlayaDeEstacionamiento:
    def __init__(self):
        self.sectores = [None] * NUM_SECTORES
        self.cola_cobro = queue.Queue(maxsize=2)
        self.eventos = []
        self.recaudacion_total = 0
        self.tiempo_uso_sectores = [0] * NUM_SECTORES
        self.tiempo_espera_cobro_total = 0
        self.autos_atendidos = 0
        self.autos_rechazados = 0
        self.vector_estado = []

    def agregar_evento(self, tiempo, tipo_evento, auto=None, sector=None):
        self.eventos.append((tiempo, tipo_evento, auto, sector))
        self.eventos.sort(key=lambda x: x[0])

    def mostrar_vector_estado(self, tiempo, tipo_evento, auto, sector,datos_random):

        porcentaje_utilizacion = sum(self.tiempo_uso_sectores) / (NUM_SECTORES * DURACION_SIMULACION) * 100
        tiempo_promedio_espera_cobro = self.tiempo_espera_cobro_total / self.autos_atendidos if self.autos_atendidos > 0 else 0
        estado = {
            "tiempo": tiempo,
            "tipo_evento": tipo_evento,
            "auto_actual": datos_random[:4] if datos_random and len(datos_random) >= 4 else "No llego un auto",
            "proxima_llegada": datos_random[4:7] if datos_random and len(datos_random) >= 7 else "No llegara otro auto",
            "sectores": [(f"Lugar:{i + 1}", f"{sector_auto.__repr__()}" if sector_auto else "Libre") for i, sector_auto in enumerate(self.sectores)],
            "cola_cobro": self.cola_cobro.qsize(),
            "proximos_eventos": [(evento[0], evento[1], evento[2].id if evento[2] else "N/A", evento[3]) for evento in self.eventos],
            "recaudacion_total": self.recaudacion_total,
            "autos_atendidos": self.autos_atendidos,
            "autos_rechazados": self.autos_rechazados,
            "porcentaje_utilizacion":porcentaje_utilizacion,
            "tiempo_promedio_espera":tiempo_promedio_espera_cobro,
            
        }
        self.vector_estado.append(estado)
        
        # Escribir estado en un archivo JSON
        with open("estado_simulacion.json", "w") as file:
            json.dump(self.vector_estado, file, indent=4)
        

    def seleccionar_tipo_auto(self):
        rnd_tipo = round(random.random(),4)
        if rnd_tipo == 1:
            rnd_tipo -= 0.001
        cumulative_probability = 0.0
        for tipo, probabilidad in PROBABILIDADES_TIPO.items():
            cumulative_probability += probabilidad
            if rnd_tipo <= cumulative_probability:
                return tipo, rnd_tipo

    def seleccionar_tiempo_estacionamiento(self):
        rnd_tiempo = round(random.random(),4)
        if rnd_tiempo == 1:
            rnd_tiempo -= 0.001
        cumulative_probability = 0.0
        for tiempo, probabilidad in PROBABILIDADES_TIEMPO.items():
            cumulative_probability += probabilidad
            if rnd_tiempo <= cumulative_probability:
                return tiempo, rnd_tiempo   
    def proximo_auto(self):
        rnd_prox = random.random()
        if rnd_prox == 1:
            rnd_prox -= 0.001
        tiempo_entre_llegada = int(round(-TIEMPO_ENTRE_LLEGADAS * math.log(1 - rnd_prox),0))

        return rnd_prox, tiempo_entre_llegada



    def llegada_auto(self, tiempo):
        tipo_auto, rnd_tipo = self.seleccionar_tipo_auto()
        tiempo_estacionamiento, rnd_tiempo = self.seleccionar_tiempo_estacionamiento()
        auto = Auto(tipo_auto, tiempo_estacionamiento,estado="Estacionado")
        auto.tiempo_llegada = tiempo

        #datos para el vector estado
        datos_randoms_actual = [rnd_tipo,tipo_auto,rnd_tiempo,tiempo_estacionamiento]        

        # Buscar un sector vacío
        sector_vacio = None
        for i in range(NUM_SECTORES):
            if self.sectores[i] is None:
                sector_vacio = i
                break

        if sector_vacio is not None:
            self.sectores[sector_vacio] = auto
            self.agregar_evento(tiempo + auto.tiempo_estacionamiento, 'salida_auto', auto, sector_vacio)
        else:
            self.autos_rechazados += 1

        # Agregar el próximo evento de llegada de auto
        rnd_prox_llegada , tiempo_entre_llegada = self.proximo_auto()
        datos_randoms_actual.extend([rnd_prox_llegada , tiempo_entre_llegada,tiempo + tiempo_entre_llegada])
        self.agregar_evento(tiempo + tiempo_entre_llegada, 'llegada_auto')

        # Mostrar el vector de estado después de cada llegada de auto
        self.mostrar_vector_estado(tiempo, 'llegada_auto', auto, sector_vacio,datos_randoms_actual)

    def salida_auto(self, tiempo, auto, sector):
        if not self.cola_cobro.full():
            auto.tiempo_inicio_cobro = tiempo
            auto.estado = "Pagando"
            self.cola_cobro.put(auto)
            self.agregar_evento(tiempo + 2, 'fin_cobro', auto, sector)
        else:
            self.agregar_evento(tiempo + 1, 'salida_auto', auto, sector)

        self.mostrar_vector_estado(tiempo, 'salida_auto', auto, sector,None)

    def fin_cobro(self, tiempo, auto, sector):
        self.sectores[sector] = None
        self.recaudacion_total += (auto.tiempo_estacionamiento / 60) * COSTO_POR_HORA[auto.tipo]
        self.tiempo_uso_sectores[sector] += auto.tiempo_estacionamiento
        auto.tiempo_espera_cobro = tiempo - auto.tiempo_inicio_cobro
        self.tiempo_espera_cobro_total += auto.tiempo_espera_cobro
        self.autos_atendidos += 1

        self.mostrar_vector_estado(tiempo, 'fin_cobro', auto, sector,None)

        if not self.cola_cobro.empty():
            siguiente_auto = self.cola_cobro.get()
            self.agregar_evento(tiempo + 2, 'fin_cobro', siguiente_auto, sector)

    def ejecutar_simulacion(self):
        self.agregar_evento(0, 'llegada_auto')

        while self.eventos:
            tiempo, tipo_evento, auto, sector = self.eventos.pop(0)
            if tiempo > DURACION_SIMULACION:
                self.mostrar_vector_estado(tiempo,tipo_evento,auto,sector,None)
                break
            if tipo_evento == 'llegada_auto':
                self.llegada_auto(tiempo)
            elif tipo_evento == 'salida_auto':
                self.salida_auto(tiempo, auto, sector)
            elif tipo_evento == 'fin_cobro':
                self.fin_cobro(tiempo, auto, sector)

# Datos de ejemplo
def iniciar_simulacion():
    playa = PlayaDeEstacionamiento()
    playa.ejecutar_simulacion()

    data = playa.vector_estado
    # Obtener valores de los campos de entrada
    tiempo = tiempo_entry.get()
    iteraciones = int(iteraciones_entry.get())
    hora_inicio = hora_inicio_entry.get()

    # Limpiar la tabla
    for row in tree.get_children():
        tree.delete(row)

    # Mostrar los datos en la tabla
    for i in range(min(iteraciones, len(data))):
        item = data[i]
        auto_actual = item["auto_actual"]
        proxima_llegada = item["proxima_llegada"]
        sectores = item["sectores"]
        
        if auto_actual == "No llego un auto":
            auto_actual_data = ['-', '-', '-', '-', True]
        else:
            auto_actual_data = [*auto_actual,False]
        
        if proxima_llegada == "No llegara otro auto":
            proxima_llegada_data = ['-', '-', '-', True]
        else:
            proxima_llegada_data = [*proxima_llegada,False]
        
        sector_data = []
        for sector in sectores:
            if len(sector) == 2:
                sector_data.append(sector[1])
            else:
                sector_data.append("Libre")
        
        tree.insert('', 'end', values=(
            item["tiempo"],
            item["tipo_evento"],
            *auto_actual_data[:4], auto_actual_data[4] if len(auto_actual_data) > 4 else False,
            *proxima_llegada_data[:3], proxima_llegada_data[3] if len(proxima_llegada_data) > 3 else False,
            *sector_data,
            item["cola_cobro"],
            str(item["proximos_eventos"]),
            item["recaudacion_total"],
            item["autos_atendidos"],
            item["autos_rechazados"],
            item["porcentaje_utilizacion"],
            item["tiempo_promedio_espera"]
        ))
    
    # Agregar fila extra con el último elemento del array
    ultima_fila = data[-1]
    auto_actual = ultima_fila["auto_actual"]
    proxima_llegada = ultima_fila["proxima_llegada"]
    sectores = ultima_fila["sectores"]

    if auto_actual == "No llego un auto":
            auto_actual_data = ['-', '-', '-', '-', True]
    else:
            auto_actual_data = [*auto_actual,False]
        
    if proxima_llegada == "No llegara otro auto":
            proxima_llegada_data = ['-', '-', '-', True]
    else:
            proxima_llegada_data = [*proxima_llegada,False]
    sector_data = []
    for sector in sectores:
        if len(sector) == 2:
            sector_data.append(sector[1])
        else:
            sector_data.append("Libre")
        
    tree.insert('', 'end', values=(
        ultima_fila["tiempo"],
        ultima_fila["tipo_evento"],
        *auto_actual_data[:4], auto_actual_data[4] if len(auto_actual_data) > 4 else False,
        *proxima_llegada_data[:3], proxima_llegada_data[3] if len(proxima_llegada_data) > 3 else False,
        *sector_data,
        ultima_fila["cola_cobro"],
        str(ultima_fila["proximos_eventos"]),
        ultima_fila["recaudacion_total"],
        ultima_fila["autos_atendidos"],
        ultima_fila["autos_rechazados"],
        ultima_fila["porcentaje_utilizacion"],
        ultima_fila["tiempo_promedio_espera"]
    ), tags=('ultima',))
    tree.tag_configure('ultima', background='lightgrey')


if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Simulación de Datos")
    root.geometry("1200x800")

    # Crear el frame para los campos de entrada
    input_frame = tk.Frame(root)
    input_frame.pack(pady=20)

    # Campo de entrada para el parámetro de tiempo
    tk.Label(input_frame, text="Parámetro de Tiempo:").grid(row=0, column=0, padx=10, pady=5)
    tiempo_entry = tk.Entry(input_frame)
    tiempo_entry.grid(row=0, column=1, padx=10, pady=5)

    # Campo de entrada para el parámetro de iteraciones
    tk.Label(input_frame, text="Iteraciones:").grid(row=1, column=0, padx=10, pady=5)
    iteraciones_entry = tk.Entry(input_frame)
    iteraciones_entry.grid(row=1, column=1, padx=10, pady=5)

    # Campo de entrada para la hora de inicio
    tk.Label(input_frame, text="Hora de Inicio:").grid(row=2, column=0, padx=10, pady=5)
    hora_inicio_entry = tk.Entry(input_frame)
    hora_inicio_entry.grid(row=2, column=1, padx=10, pady=5)

    # Botón para iniciar la simulación
    start_button = tk.Button(input_frame, text="Iniciar Simulación", command=iniciar_simulacion)
    start_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Crear el treeview con scrollbars
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    columns = (
        "Tiempo", "Tipo Evento", "RND Tamaño", "Tamaño", "RND Tiempo Estacionamiento", "Tiempo Estacionamiento", "No Llego Un Auto (Actual)",
        "RND Próx Llegada", "Tiempo Entre Llegadas", "Próxima Llegada", "No Llega Un Auto (Próxima)",
        "Sector 1", "Sector 2", "Sector 3", "Sector 4", "Sector 5", "Sector 6", "Sector 7", "Sector 8",
        "Cola Cobro", "Próximos Eventos", "Recaudación Total", "Autos Atendidos", "Autos Rechazados", "Porcentaje Utilización", "Tiempo Promedio Espera"
    )

    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar vertical
    scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar_y.set)

    # Scrollbar horizontal
    scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=scrollbar_x.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    root.mainloop()

        



