import random
import queue
import json
import tkinter as tk
from tkinter import ttk
import math

# Parámetros de la simulación
NUM_SECTORES = 8
TIEMPO_ENTRE_LLEGADAS = 13  # minutos
DURACION_SIMULACION = 8 * 60 # minutos (8 horas)

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

    def mostrar_vector_estado(self, tiempo, tipo_evento, auto, sector, datos_random):
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
            "porcentaje_utilizacion": porcentaje_utilizacion,
            "tiempo_promedio_espera": tiempo_promedio_espera_cobro,
        }
        self.vector_estado.append(estado)
        
        # Escribir estado en un archivo JSON
        with open("estado_simulacion.json", "w") as file:
            json.dump(self.vector_estado, file, indent=4)

    def seleccionar_tipo_auto(self):
        rnd_tipo = round(random.random(), 4)
        if rnd_tipo == 1:
            rnd_tipo -= 0.001
        cumulative_probability = 0.0
        for tipo, probabilidad in PROBABILIDADES_TIPO.items():
            cumulative_probability += probabilidad
            if rnd_tipo <= cumulative_probability:
                return tipo, rnd_tipo

    def seleccionar_tiempo_estacionamiento(self):
        rnd_tiempo = round(random.random(), 4)
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
        tiempo_entre_llegada = int(round(-TIEMPO_ENTRE_LLEGADAS * math.log(1 - rnd_prox), 0))

        return rnd_prox, tiempo_entre_llegada

    def llegada_auto(self, tiempo):
        tipo_auto, rnd_tipo = self.seleccionar_tipo_auto()
        tiempo_estacionamiento, rnd_tiempo = self.seleccionar_tiempo_estacionamiento()
        auto = Auto(tipo_auto, tiempo_estacionamiento, estado="Estacionado")
        auto.tiempo_llegada = tiempo

        # Datos para el vector estado
        datos_randoms_actual = [rnd_tipo, tipo_auto, rnd_tiempo, tiempo_estacionamiento]

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
        rnd_prox_llegada, tiempo_entre_llegada = self.proximo_auto()
        datos_randoms_actual.extend([rnd_prox_llegada, tiempo_entre_llegada, tiempo + tiempo_entre_llegada])
        self.agregar_evento(tiempo + tiempo_entre_llegada, 'llegada_auto')

        # Mostrar el vector de estado después de cada llegada de auto
        self.mostrar_vector_estado(tiempo, 'llegada_auto', auto, sector_vacio, datos_randoms_actual)

    def salida_auto(self, tiempo, auto, sector):
        if not self.cola_cobro.full():
            auto.tiempo_inicio_cobro = tiempo
            auto.estado = "Pagando"
            self.cola_cobro.put(auto)
            self.agregar_evento(tiempo + 2, 'fin_cobro', auto, sector)
        else:
            self.agregar_evento(tiempo + 1, 'salida_auto', auto, sector)

        self.mostrar_vector_estado(tiempo, 'salida_auto', auto, sector, None)

    def fin_cobro(self, tiempo, auto, sector):
        self.sectores[sector] = None
        self.recaudacion_total += (auto.tiempo_estacionamiento / 60) * COSTO_POR_HORA[auto.tipo]
        self.tiempo_uso_sectores[sector] += auto.tiempo_estacionamiento
        auto.tiempo_espera_cobro = tiempo - auto.tiempo_inicio_cobro
        self.tiempo_espera_cobro_total += auto.tiempo_espera_cobro
        self.autos_atendidos += 1

        self.mostrar_vector_estado(tiempo, 'fin_cobro', auto, sector, None)

        if not self.cola_cobro.empty():
            siguiente_auto = self.cola_cobro.get()
            self.agregar_evento(tiempo + 2, 'fin_cobro', siguiente_auto, sector)

    def ejecutar_simulacion(self):
        self.agregar_evento(0, 'llegada_auto')

        while self.eventos:
            tiempo, tipo_evento, auto, sector = self.eventos.pop(0)
            if tiempo > DURACION_SIMULACION:
                self.mostrar_vector_estado(tiempo, tipo_evento, auto, sector, None)
                break
            if tipo_evento == 'llegada_auto':
                self.llegada_auto(tiempo)
            elif tipo_evento == 'salida_auto':
                self.salida_auto(tiempo, auto, sector)
            elif tipo_evento == 'fin_cobro':
                self.fin_cobro(tiempo, auto, sector)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Playa de Estacionamiento")
        self.create_widgets()

    def create_widgets(self):
        self.tipo_autos_labels = {}
        self.tipo_autos_entries = {}
        self.tiempo_estacionamiento_labels = {}
        self.tiempo_estacionamiento_entries = {}
        
        # Labels y entries para probabilidades de tipo de auto
        for i, (tipo, prob) in enumerate(PROBABILIDADES_TIPO.items()):
            label = tk.Label(self.root, text=f"Probabilidad {tipo.capitalize()}:")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.tipo_autos_labels[tipo] = label
            
            entry = tk.Entry(self.root)
            entry.insert(0, str(prob))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.tipo_autos_entries[tipo] = entry

        # Labels y entries para probabilidades de tiempo de estacionamiento
        for i, (tiempo, prob) in enumerate(PROBABILIDADES_TIEMPO.items(), start=len(PROBABILIDADES_TIPO)):
            label = tk.Label(self.root, text=f"Probabilidad {tiempo} minutos:")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.tiempo_estacionamiento_labels[tiempo] = label
            
            entry = tk.Entry(self.root)
            entry.insert(0, str(prob))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.tiempo_estacionamiento_entries[tiempo] = entry

        self.run_button = tk.Button(self.root, text="Iniciar Simulación", command=self.run_simulation)
        self.run_button.grid(row=len(PROBABILIDADES_TIPO) + len(PROBABILIDADES_TIEMPO), column=0, columnspan=2, pady=10)
        
        self.result_text = tk.Text(self.root, wrap=tk.WORD, height=15, width=80)
        self.result_text.grid(row=len(PROBABILIDADES_TIPO) + len(PROBABILIDADES_TIEMPO) + 1, column=0, columnspan=2, pady=10)
    
    def run_simulation(self):
        for tipo, entry in self.tipo_autos_entries.items():
            PROBABILIDADES_TIPO[tipo] = float(entry.get())

        for tiempo, entry in self.tiempo_estacionamiento_entries.items():
            PROBABILIDADES_TIEMPO[int(tiempo)] = float(entry.get())

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Ejecutando simulación...\n")

        playa = PlayaDeEstacionamiento()
        playa.ejecutar_simulacion()

        self.result_text.insert(tk.END, f"Recaudación Total: {playa.recaudacion_total}\n")
        self.result_text.insert(tk.END, f"Autos Atendidos: {playa.autos_atendidos}\n")
        self.result_text.insert(tk.END, f"Autos Rechazados: {playa.autos_rechazados}\n")
        self.result_text.insert(tk.END, f"Porcentaje de Utilización: {sum(playa.tiempo_uso_sectores) / (NUM_SECTORES * DURACION_SIMULACION) * 100:.2f}%\n")
        self.result_text.insert(tk.END, f"Tiempo Promedio de Espera en Cobro: {playa.tiempo_espera_cobro_total / playa.autos_atendidos if playa.autos_atendidos > 0 else 0:.2f} minutos\n")

        # Mostrar el vector de estado
        self.result_text.insert(tk.END, "\nVector de Estado:\n")
        for estado in playa.vector_estado:
            self.result_text.insert(tk.END, f"Tiempo: {estado['tiempo']} - Tipo de Evento: {estado['tipo_evento']}\n")
            self.result_text.insert(tk.END, f"Auto Actual: {estado['auto_actual']}\n")
            self.result_text.insert(tk.END, f"Próxima Llegada: {estado['proxima_llegada']}\n")
            self.result_text.insert(tk.END, "Sectores:\n")
            for sector in estado['sectores']:
                self.result_text.insert(tk.END, f"    {sector[0]}: {sector[1]}\n")
            self.result_text.insert(tk.END, f"Cola Cobro: {estado['cola_cobro']}\n")
            self.result_text.insert(tk.END, f"Próximos Eventos: {estado['proximos_eventos']}\n")
            self.result_text.insert(tk.END, f"Recaudación Total: {estado['recaudacion_total']}\n")
            self.result_text.insert(tk.END, f"Autos Atendidos: {estado['autos_atendidos']}\n")
            self.result_text.insert(tk.END, f"Autos Rechazados: {estado['autos_rechazados']}\n")
            self.result_text.insert(tk.END, f"Porcentaje de Utilización: {estado['porcentaje_utilizacion']:.2f}%\n")
            self.result_text.insert(tk.END, f"Tiempo Promedio de Espera: {estado['tiempo_promedio_espera']:.2f} minutos\n\n")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
