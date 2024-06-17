import random
import queue
import json

# Parámetros de la simulación
NUM_SECTORES = 8
TIEMPO_ENTRE_LLEGADAS = 13  # minutos
DURACION_SIMULACION = 13 # minutos (8 horas)

# Costos de estacionamiento por tipo de auto
COSTO_POR_HORA = {
    'pequeño': 300,
    'grande': 500,
    'utilitario': 1000
}

# Probabilidades de tipo de auto
PROBABILIDADES_TIPO = {
    'pequeño': 0.45,
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

    def __init__(self, tipo, tiempo_estacionamiento):
        self.id = Auto._id_counter
        Auto._id_counter += 1
        self.tipo = tipo
        self.tiempo_estacionamiento = tiempo_estacionamiento
        self.tiempo_llegada = None
        self.tiempo_salida = None
        self.tiempo_inicio_cobro = None
        self.tiempo_espera_cobro = None

    def __repr__(self):
        return f"Auto {self.id} (Tipo: {self.tipo})"

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

    def agregar_evento(self, tiempo, tipo_evento, auto=None, sector=None):
        self.eventos.append((tiempo, tipo_evento, auto, sector))
        self.eventos.sort()

    def mostrar_vector_estado(self, tiempo, tipo_evento, auto, sector):
        evento_auto = auto.id if auto else "N/A"

        vector_estado = [tiempo,tipo_evento,self.sectores,self.eventos[0],self.recaudacion_total,self.autos_atendidos,self.autos_rechazados]
        # vector_estado = [tiempo,tipo_evento,self.sectores,self.cola_cobro,self.eventos[0] -> prox evento,self.sectores,self.recaudacion_total,self.autos_atendidos,self.autos_rechazados]
        print(vector_estado)
        #with open('vector_Estado.json', 'w') as jf: 
        #   json.dump(vector_estado, jf, ensure_ascii=False, indent=2)

        print("Hora simulada:", tiempo)
        print("Evento simulado:", tipo_evento, f"({evento_auto})")
        print("Próximos eventos:")
        for evento in self.eventos:
            evento_auto = evento[2].id if evento[2] else "N/A"
            print(f"\tTiempo: {evento[0]} , Tipo: {evento[1]}, Auto: {evento_auto}, Sector: {evento[3]}")


        print("Sectores:")
        for i, sector_auto in enumerate(self.sectores):
            if sector_auto:
                print(f"\tSector {i+1}: Tipo: {sector_auto.tipo}, Llegada: {sector_auto.tiempo_llegada}, Estac.: {sector_auto.tiempo_estacionamiento}")
            else:
                print(f"\tSector {i+1}: Vacío")

        print("Recaudación total:", self.recaudacion_total)
        print("Autos atendidos:", self.autos_atendidos)
        print("Autos rechazados:", self.autos_rechazados)
        print("-" * 50)

    def llegada_auto(self, tiempo):
        tipo_auto = random.choices(list(PROBABILIDADES_TIPO.keys()), list(PROBABILIDADES_TIPO.values()))[0]
        tiempo_estacionamiento = random.choices(list(PROBABILIDADES_TIEMPO.keys()), list(PROBABILIDADES_TIEMPO.values()))[0]
        auto = Auto(tipo_auto, tiempo_estacionamiento)
        auto.tiempo_llegada = tiempo

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
        self.agregar_evento(tiempo + TIEMPO_ENTRE_LLEGADAS, 'llegada_auto')

        # Mostrar el vector de estado después de cada llegada de auto
        self.mostrar_vector_estado(tiempo, 'llegada_auto', auto, sector_vacio)

    def salida_auto(self, tiempo, auto, sector):
        if not self.cola_cobro.full():
            auto.tiempo_inicio_cobro = tiempo
            self.cola_cobro.put(auto)
            self.agregar_evento(tiempo + 2, 'fin_cobro', auto, sector)
        else:
            self.agregar_evento(tiempo + 1, 'salida_auto', auto, sector)

        self.mostrar_vector_estado(tiempo, 'salida_auto', auto, sector)

    def fin_cobro(self, tiempo, auto, sector):
        self.sectores[sector] = None
        self.recaudacion_total += (auto.tiempo_estacionamiento / 60) * COSTO_POR_HORA[auto.tipo]
        self.tiempo_uso_sectores[sector] += auto.tiempo_estacionamiento
        auto.tiempo_espera_cobro = tiempo - auto.tiempo_inicio_cobro
        self.tiempo_espera_cobro_total += auto.tiempo_espera_cobro
        self.autos_atendidos += 1

        self.mostrar_vector_estado(tiempo, 'fin_cobro', auto, sector)

        if not self.cola_cobro.empty():
            siguiente_auto = self.cola_cobro.get()
            self.agregar_evento(tiempo + 2, 'fin_cobro', siguiente_auto, sector)

    def ejecutar_simulacion(self):
        self.agregar_evento(0, 'llegada_auto')

        while self.eventos:
            tiempo, tipo_evento, auto, sector = self.eventos.pop(0)
            if tiempo > DURACION_SIMULACION:
                break
            if tipo_evento == 'llegada_auto':
                self.llegada_auto(tiempo)
            elif tipo_evento == 'salida_auto':
                self.salida_auto(tiempo, auto, sector)
            elif tipo_evento == 'fin_cobro':
                self.fin_cobro(tiempo, auto, sector)

        # Calcular métricas finales
        porcentaje_utilizacion = sum(self.tiempo_uso_sectores) / (NUM_SECTORES * DURACION_SIMULACION) * 100
        tiempo_promedio_espera_cobro = self.tiempo_espera_cobro_total / self.autos_atendidos if self.autos_atendidos > 0 else 0

        return {
            "recaudacion_total": self.recaudacion_total,
            "porcentaje_utilizacion": porcentaje_utilizacion,
            "tiempo_promedio_espera_cobro": tiempo_promedio_espera_cobro
        }

if __name__ == "__main__":
    playa = PlayaDeEstacionamiento()
    resultados = playa.ejecutar_simulacion()

    print("Recaudación Total: $", resultados["recaudacion_total"])
    print("Porcentaje de Utilización de la Playa: {:.2f}%".format(resultados["porcentaje_utilizacion"]))
    print("Promedio de Tiempo de Espera por el Cobro: {:.2f} minutos".format(resultados["tiempo_promedio_espera_cobro"]))
