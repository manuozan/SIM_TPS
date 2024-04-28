import random

# Definir las probabilidades dadas
p_no_responder = 0.10
p_recordar_mensaje = 0.40
p_no_recordar_mensaje = 0.50

# Probabilidades condicionales de respuesta a la pregunta de compra
p_definitivamente_no_recordar = 0.30
p_dudoso_recordar = 0.30
p_definitivamente_si_recordar = 0.40

p_definitivamente_no_no_recordar = 0.50
p_dudoso_no_recordar = 0.40
p_definitivamente_si_no_recordar = 0.10

# Función para generar una muestra aleatoria
def generar_muestra():
    # Simular si el individuo responde o no
    responde = random.random() > p_no_responder

    if responde:
        # Simular si el individuo recuerda el mensaje
        recuerda_mensaje = random.random() < p_recordar_mensaje

        # Simular la respuesta a la pregunta de compra
        if recuerda_mensaje:
            p_definitivamente_si = p_definitivamente_si_recordar
            p_dudoso = p_dudoso_recordar
            p_definitivamente_no = p_definitivamente_no_recordar
        else:
            p_definitivamente_si = p_definitivamente_si_no_recordar
            p_dudoso = p_dudoso_no_recordar
            p_definitivamente_no = p_definitivamente_no_no_recordar

        # Generar una muestra aleatoria de la respuesta
        muestra = random.random()
        if muestra < p_definitivamente_si:
            return 1  # Definitivamente sí
        elif muestra < p_definitivamente_si + p_dudoso:
            return 0  # Dudoso
        else:
            return 0  # Definitivamente no
    else:
        return 0  # No responde

# Función para realizar la simulación de Monte Carlo
def simulacion_monte_carlo(n):
    contador_definitivamente_si = 0
    for _ in range(n):
        if generar_muestra() == 1:
            contador_definitivamente_si += 1
    return contador_definitivamente_si / n

# Realizar la simulación de Monte Carlo con 100,000 muestras
probabilidad_definitivamente_si = simulacion_monte_carlo(100000)
print(f"La probabilidad general de que un individuo responda 'definitivamente sí' a la pregunta sobre posibilidad de compra es: {probabilidad_definitivamente_si:.4f}")