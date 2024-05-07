import random

# Función para generar una muestra aleatoria
def generar_muestra(p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                    p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                    p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar):
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
            return 1, 0, 0, 0  # Definitivamente sí
        elif muestra < p_definitivamente_si + p_dudoso:
            return 0, 1, 0, 0  # Dudoso
        else:
            return 0, 0, 1, 0  # Definitivamente no
    else:
        return 0, 0, 0, 1  # No responde

# Función para realizar la simulación de Monte Carlo
def simulacion_monte_carlo(n, tiempo_simulado, inicio_iteraciones, p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                    p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                    p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar):
    # Inicializar acumuladores
    contador_definitivamente_si = 0
    contador_dudoso = 0
    contador_definitivamente_no = 0
    contador_no_responde = 0

    # Inicializar vector de estado
    vector_estado = []

    # Iniciar simulación
    for i in range(1, n + 1):
        # Generar muestra
        muestra = generar_muestra(p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                                   p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                                   p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar)
        
        # Actualizar acumuladores
        contador_definitivamente_si += muestra[0]
        contador_dudoso += muestra[1]
        contador_definitivamente_no += muestra[2]
        contador_no_responde += muestra[3]

        # Actualizar vector de estado
        if i >= inicio_iteraciones and i % tiempo_simulado == 0:
            probabilidad_acumulada = contador_definitivamente_si / (contador_definitivamente_si + contador_dudoso + contador_definitivamente_no + contador_no_responde)
            vector_estado.append((i, contador_definitivamente_si, contador_dudoso, contador_definitivamente_no, contador_no_responde, probabilidad_acumulada))

    return vector_estado, (i, contador_definitivamente_si, contador_dudoso, contador_definitivamente_no, contador_no_responde, probabilidad_acumulada)

# Función para mostrar el vector de estado
def mostrar_vector_estado(vector_estado):
    print("Vector de estado:")
    print("Iteración\tDefinitivamente Sí\tDudoso\tDefinitivamente No\tNo Responde\tProbabilidad Acumulada")
    for estado in vector_estado:
        print(f"{estado[0]}\t\t{estado[1]}\t\t\t{estado[2]}\t\t{estado[3]}\t\t\t{estado[4]}\t\t{round(estado[5],4)}")

# Función para mostrar la fila N
def mostrar_ultima_fila(acumuladores):
    print("\nÚltima fila simulada:")
    print("Iteración\tDefinitivamente Sí\tDudoso\tDefinitivamente No\tNo Responde\tProbabilidad Acumulada")
    print(f"{acumuladores[0]}\t\t{acumuladores[1]}\t\t\t{acumuladores[2]}\t\t{acumuladores[3]}\t\t\t{acumuladores[4]}\t\t{acumuladores[5]}")

# Función para mostrar el menú
def menu():
    print("\nSimulación de Monte Carlo - Anuncio por Televisión")
    print("1. Cargar valores personalizados")
    print("2. Cargar valores predefinidos")
    print("0. Salir")

# Iniciar el programa
while True:
    menu()
    opcion = input("Seleccione una opción: ")

 
        
    if opcion == "1":
        tiempo_simulado = int(input("Ingrese el tiempo de simulación: "))
        inicio_iteraciones = int(input("Ingrese el inicio de las iteraciones a mostrar: "))
        p_no_responder = float(input("Ingrese la probabilidad de no responder: "))
        p_recordar_mensaje = float(input("Ingrese la probabilidad de recordar el mensaje: "))
        p_no_recordar_mensaje = float(input("Ingrese la probabilidad de no recordar el mensaje: "))
        p_definitivamente_no_recordar = float(input("Ingrese la probabilidad de definitivamente no recordar el mensaje: "))
        p_dudoso_recordar = float(input("Ingrese la probabilidad de dudar al recordar el mensaje: "))
        p_definitivamente_si_recordar = float(input("Ingrese la probabilidad de definitivamente sí recordar el mensaje: "))
        p_definitivamente_no_no_recordar = float(input("Ingrese la probabilidad de definitivamente no no recordar el mensaje: "))
        p_dudoso_no_recordar = float(input("Ingrese la probabilidad de dudar al no recordar el mensaje: "))
        p_definitivamente_si_no_recordar = float(input("Ingrese la probabilidad de definitivamente sí no recordar el mensaje: "))
        cantidad_iteraciones = int(input("Ingrese la cantidad de iteraciones totales: "))

        vector_estado, ultima_fila = simulacion_monte_carlo(cantidad_iteraciones, tiempo_simulado, inicio_iteraciones,
                                                             p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                                                             p_definitivamente_no_recordar, p_dudoso_recordar,
                                                             p_definitivamente_si_recordar, p_definitivamente_no_no_recordar,
                                                             p_dudoso_no_recordar, p_definitivamente_si_no_recordar)
        
        mostrar_vector_estado(vector_estado)
        mostrar_ultima_fila(ultima_fila)

    elif opcion == "2":
        tiempo_simulado = int(input("Ingrese el tiempo de simulación: "))
        inicio_iteraciones = int(input("Ingrese el inicio de las iteraciones a mostrar: "))
        p_no_responder = 0.1
        p_recordar_mensaje = 0.4
        p_no_recordar_mensaje = 0.5
        p_definitivamente_no_recordar = 0.3
        p_dudoso_recordar = 0.3
        p_definitivamente_si_recordar = 0.4
        p_definitivamente_no_no_recordar = 0.5
        p_dudoso_no_recordar = 0.4
        p_definitivamente_si_no_recordar = 0.1
        cantidad_iteraciones = int(input("Ingrese la cantidad de iteraciones totales: "))

        vector_estado, ultima_fila = simulacion_monte_carlo(cantidad_iteraciones, tiempo_simulado, inicio_iteraciones,
                                                             p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                                                             p_definitivamente_no_recordar, p_dudoso_recordar,
                                                             p_definitivamente_si_recordar, p_definitivamente_no_no_recordar,
                                                             p_dudoso_no_recordar, p_definitivamente_si_no_recordar)
        
        mostrar_vector_estado(vector_estado)
        mostrar_ultima_fila(ultima_fila)
        
    elif opcion == "0":
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
