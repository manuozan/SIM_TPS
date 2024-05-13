import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random



def generar_muestra(p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                    p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                    p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar):
    # Simular si el individuo responde o no
    random_resp = round(random.random(),4)
    if random_resp == 1:
        random_resp -= 0.0001

    responde =  random_resp > p_no_responder
    
    # Variable auxiliar para saber que string devolver segun recuerda o no
    recuerda_mensaje_resultado = ""
    #Se niega a responder el mensaje, se corta la simulacion
    if responde == False:
        return 0,0,0,1,random_resp,"Se nego a responder","-","-"
    #Saber si el individuo recuerda o no el mensaje
    recuerda_mensaje = random_resp < p_recordar_mensaje + p_no_responder
    #Si lo recuerda por lo que las probabilidades se van a basar en eso
    if recuerda_mensaje:
        p_definitivamente_si = p_definitivamente_si_recordar
        p_dudoso = p_dudoso_recordar
        p_definitivamente_no = p_definitivamente_no_recordar
        recuerda_mensaje_resultado = "Recuerda el mensaje"

    else:
        p_definitivamente_si = p_definitivamente_si_no_recordar
        p_dudoso = p_dudoso_no_recordar
        p_definitivamente_no = p_definitivamente_no_no_recordar
        recuerda_mensaje_resultado = "No recuerda el mensaje"  

    #Con las probabilidades ajustadas entonces pasamos a ver si compraria el producto o no
    random_muestra = round(random.random(),4)
    if random_muestra == 1:
        random_muestra -= 0.0001
    #Definitivamente no
    if random_muestra < p_definitivamente_no:
        return 0,0,1,0,random_resp,recuerda_mensaje_resultado,random_muestra,"Definitivamente no"
    #Dudoso
    elif random_muestra < p_definitivamente_no + p_dudoso:
        return 0,1,0,0,random_resp,recuerda_mensaje_resultado,random_muestra,"Dudoso"
    #Definitivamente si
    else:
        return 1,0,0,0,random_resp,recuerda_mensaje_resultado,random_muestra,"Definitivamente si"
    



    




# Función para realizar la simulación de Monte Carlo
def simulacion_monte_carlo(n, inicio_iteraciones, fin_iteraciones, p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
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
    for i in range(1, n + 1):  # Empezar desde 1 y sumar 1 al total para obtener 100 iteraciones exactas
        # Generar muestra
        muestra = generar_muestra(p_no_responder,p_recordar_mensaje, p_no_recordar_mensaje,
                                   p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                                   p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar)

        # Actualizar acumuladores
        contador_definitivamente_si += muestra[0]
        contador_dudoso += muestra[1]
        contador_definitivamente_no += muestra[2]
        contador_no_responde += muestra[3]
        random_resp = muestra[4]
        random_resp_string = muestra[5]
        random_muestra = muestra[6]
        random_muestra_string = muestra[7]
        

        # Actualizar vector de estado -> Se saco el tiempo simulado
        if inicio_iteraciones <= i:
            probabilidad_acumulada = contador_definitivamente_si / (contador_definitivamente_si + contador_dudoso + contador_definitivamente_no + contador_no_responde)
            vector_estado.append((i,random_resp,random_resp_string,random_muestra,random_muestra_string, contador_definitivamente_si, contador_dudoso, contador_definitivamente_no, contador_no_responde, probabilidad_acumulada))

    return vector_estado

# Función para mostrar el vector de estado
def mostrar_vector_estado(vector_estado, inicio_iteraciones, fin_iteraciones):
    output = "Vector de estado:\n\n"
    output += "{:<15} {:<20} {:<25} {:<25} {:<25} {:<20} {:<15} {:<20} {:<15} {:<25}\n".format("Iteración","Rnd responde","Respuesta","Rnd Compra","Compra", "Definitivamente Sí", "Dudoso", "Definitivamente No", "No Responde", "P(x) AC")
    
    for estado in vector_estado:
        iteracion,random_resp,random_resp_string,random_muestra,random_muestra_string,definitivamente_si, dudoso, definitivamente_no, no_responde, probabilidad_acumulada = estado
        probabilidad_acumulada = round(probabilidad_acumulada, 2)  # Redondear la probabilidad a dos decimales
        if inicio_iteraciones <= iteracion <= fin_iteraciones:
            output += "{:<15} {:<20} {:<25} {:<25} {:<25} {:<20} {:<15} {:<20} {:<15} {:<25}\n".format(iteracion,random_resp,random_resp_string,random_muestra,random_muestra_string,definitivamente_si, dudoso, definitivamente_no, no_responde, probabilidad_acumulada)
    return output

# Función para mostrar la última fila
def mostrar_ultima_fila(acumuladores):
    output = "\nÚltima fila simulada:\n\n"
    output += "{:<15} {:<20} {:<25} {:<25} {:<25} {:<20} {:<15} {:<20} {:<15} {:<25}\n".format("Iteración","Rnd responde","Respuesta","Rnd Compra","Compra", "Definitivamente Sí", "Dudoso", "Definitivamente No", "No Responde", "P(x) AC")
    iteracion,random_resp,random_resp_string,random_muestra,random_muestra_string,definitivamente_si, dudoso, definitivamente_no, no_responde, probabilidad_acumulada = acumuladores
    probabilidad_acumulada = round(probabilidad_acumulada, 2)  # Redondear la probabilidad a dos decimales
    output += "{:<15} {:<20} {:<25} {:<25} {:<25} {:<20} {:<15} {:<20} {:<15} {:<25}\n".format(iteracion,random_resp,random_resp_string,random_muestra,random_muestra_string,definitivamente_si, dudoso, definitivamente_no, no_responde, probabilidad_acumulada)
    return output


# Función para realizar la simulación con los parámetros proporcionados y mostrar los resultados
def realizar_simulacion(inicio_iteraciones, fin_iteraciones, p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                        p_definitivamente_no_recordar, p_dudoso_recordar, p_definitivamente_si_recordar,
                        p_definitivamente_no_no_recordar, p_dudoso_no_recordar, p_definitivamente_si_no_recordar, cantidad_iteraciones):
    try:
        vector_estado = simulacion_monte_carlo(cantidad_iteraciones, inicio_iteraciones, fin_iteraciones,
                                               p_no_responder, p_recordar_mensaje, p_no_recordar_mensaje,
                                               p_definitivamente_no_recordar, p_dudoso_recordar,
                                               p_definitivamente_si_recordar, p_definitivamente_no_no_recordar,
                                               p_dudoso_no_recordar, p_definitivamente_si_no_recordar)
        if vector_estado is not None and len(vector_estado) > 0:
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, mostrar_vector_estado(vector_estado,inicio_iteraciones,fin_iteraciones))
            resultado_text.insert(tk.END, mostrar_ultima_fila(vector_estado[-1]))
        else:
            messagebox.showerror("Error", "La simulación no pudo realizarse correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la simulación: {str(e)}")


# Función para cargar valores predefinidos
def cargar_valores_predefinidos():
    inicio_iteraciones_var.set(1)
    fin_iteraciones_var.set(10)
    p_no_responder_var.set(0.1)
    p_recordar_mensaje_var.set(0.4)
    p_no_recordar_mensaje_var.set(0.5)
    p_definitivamente_no_recordar_var.set(0.3)
    p_dudoso_recordar_var.set(0.3)
    p_definitivamente_si_recordar_var.set(0.4)
    p_definitivamente_no_no_recordar_var.set(0.5)
    p_dudoso_no_recordar_var.set(0.4)
    p_definitivamente_si_no_recordar_var.set(0.1)

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Monte Carlo - G14 - Anuncio por Televisión")
root.state('zoomed') #inicia la ventana maximizada

# Configurar pesos para que los frames se redimensionen correctamente
root.grid_rowconfigure(2, weight=1)  # Fila donde está resultado_frame
root.grid_columnconfigure(5, weight=1)

# Frame para los parámetros de entrada
parametros_frame = ttk.LabelFrame(root, text="Probabilidad de recordar el mensaje")
parametros_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Label y Entry para la probabilidad de no responder
ttk.Label(parametros_frame, text="No responde:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
p_no_responder_var = tk.DoubleVar()
p_no_responder_entry = ttk.Entry(parametros_frame, textvariable=p_no_responder_var)
p_no_responder_entry.grid(row=2, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de recordar el mensaje
ttk.Label(parametros_frame, text="Recuerda el mensaje:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
p_recordar_mensaje_var = tk.DoubleVar()
p_recordar_mensaje_entry = ttk.Entry(parametros_frame, textvariable=p_recordar_mensaje_var)
p_recordar_mensaje_entry.grid(row=3, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de no recordar el mensaje
ttk.Label(parametros_frame, text="No recuerda el mensaje:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
p_no_recordar_mensaje_var = tk.DoubleVar()
p_no_recordar_mensaje_entry = ttk.Entry(parametros_frame, textvariable=p_no_recordar_mensaje_var)
p_no_recordar_mensaje_entry.grid(row=4, column=1, padx=5, pady=5)

# Frame para los parámetros de entrada
parametros2_frame = ttk.LabelFrame(root, text="Probabilidad de compra al recordar el mensaje")
parametros2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


# Label y Entry para la probabilidad de definitivamente no al recordar el mensaje
ttk.Label(parametros2_frame, text="Definitivamente no:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
p_definitivamente_no_recordar_var = tk.DoubleVar()
p_definitivamente_no_recordar_entry = ttk.Entry(parametros2_frame, textvariable=p_definitivamente_no_recordar_var)
p_definitivamente_no_recordar_entry.grid(row=0, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de dudar al recordar el mensaje
ttk.Label(parametros2_frame, text="Dudoso:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
p_dudoso_recordar_var = tk.DoubleVar()
p_dudoso_recordar_entry = ttk.Entry(parametros2_frame, textvariable=p_dudoso_recordar_var)
p_dudoso_recordar_entry.grid(row=1, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de definitivamente sí recordar el mensaje
ttk.Label(parametros2_frame, text="Definitivamente sí:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
p_definitivamente_si_recordar_var = tk.DoubleVar()
p_definitivamente_si_recordar_entry = ttk.Entry(parametros2_frame, textvariable=p_definitivamente_si_recordar_var)
p_definitivamente_si_recordar_entry.grid(row=2, column=1, padx=5, pady=5)

# Frame para los parámetros de entrada
parametros3_frame = ttk.LabelFrame(root, text="Probabilidad de compra al no recordar el mensaje")
parametros3_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Label y Entry para la probabilidad de definitivamente no no recordar el mensaje
ttk.Label(parametros3_frame, text="Definitivamente no:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
p_definitivamente_no_no_recordar_var = tk.DoubleVar()
p_definitivamente_no_no_recordar_entry = ttk.Entry(parametros3_frame, textvariable=p_definitivamente_no_no_recordar_var)
p_definitivamente_no_no_recordar_entry.grid(row=0, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de dudar al no recordar el mensaje
ttk.Label(parametros3_frame, text="Dudoso:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
p_dudoso_no_recordar_var = tk.DoubleVar()
p_dudoso_no_recordar_entry = ttk.Entry(parametros3_frame, textvariable=p_dudoso_no_recordar_var)
p_dudoso_no_recordar_entry.grid(row=1, column=1, padx=5, pady=5)

# Label y Entry para la probabilidad de definitivamente sí no recordar el mensaje
ttk.Label(parametros3_frame, text="Definitivamente sí:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
p_definitivamente_si_no_recordar_var = tk.DoubleVar()
p_definitivamente_si_no_recordar_entry = ttk.Entry(parametros3_frame, textvariable=p_definitivamente_si_no_recordar_var)
p_definitivamente_si_no_recordar_entry.grid(row=2, column=1, padx=5, pady=5)

# Frame para los parámetros de entrada
parametros4_frame = ttk.LabelFrame(root, text="Parámetros")
parametros4_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

# Label y Entry para la cantidad de iteraciones
ttk.Label(parametros4_frame, text="Cantidad de iteraciones:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
cantidad_iteraciones_var = tk.IntVar()
cantidad_iteraciones_entry = ttk.Entry(parametros4_frame, textvariable=cantidad_iteraciones_var)
cantidad_iteraciones_entry.grid(row=0, column=1, padx=5, pady=5)
cantidad_iteraciones_var.set(100)

# Label y Entry para el inicio de las iteraciones a mostrar
ttk.Label(parametros4_frame, text="Inicio de las iteraciones a mostrar:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
inicio_iteraciones_var = tk.IntVar()
inicio_iteraciones_entry = ttk.Entry(parametros4_frame, textvariable=inicio_iteraciones_var)
inicio_iteraciones_entry.grid(row=1, column=1, padx=5, pady=5)

# Label y Entry para el fin de las iteraciones a mostrar
ttk.Label(parametros4_frame, text="Fin de las iteraciones a mostrar:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
fin_iteraciones_var = tk.IntVar()
fin_iteraciones_entry = ttk.Entry(parametros4_frame, textvariable=fin_iteraciones_var)
fin_iteraciones_entry.grid(row=2, column=1, padx=5, pady=5)

# Frame para los botones
botones_frame = ttk.Frame(root)
botones_frame.grid(row=0, column=4, padx=10, pady=10)

# Botón para cargar valores predefinidos
predefinidos_button = ttk.Button(botones_frame, text="CARGAR VALORES\nPREDEFINIDOS", command=cargar_valores_predefinidos, width=20)
predefinidos_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Centrado horizontal y verticalmente

# Botón para realizar la simulación
simular_button = ttk.Button(botones_frame, text="REALIZAR\nSIMULACIÓN", command=lambda: realizar_simulacion(inicio_iteraciones_var.get(), fin_iteraciones_var.get(),
    p_no_responder_var.get(), p_recordar_mensaje_var.get(), p_no_recordar_mensaje_var.get(),
    p_definitivamente_no_recordar_var.get(), p_dudoso_recordar_var.get(), p_definitivamente_si_recordar_var.get(),
    p_definitivamente_no_no_recordar_var.get(), p_dudoso_no_recordar_var.get(), p_definitivamente_si_no_recordar_var.get(), cantidad_iteraciones_var.get()), width=20)
simular_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")  # Centrado horizontal y verticalmente


# Frame para el resultado
resultado_frame = ttk.LabelFrame(root, text="Resultado")
resultado_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")


# Configurar pesos para que resultado_frame se redimensione
resultado_frame.grid_rowconfigure(2, weight=1)
resultado_frame.grid_columnconfigure(0, weight=1)

# Texto para mostrar el resultado
# Crear el campo de texto para mostrar el resultado
resultado_text = tk.Text(resultado_frame, height=15, width=100)  # Ancho ajustado al número de caracteres

# Ajustar el campo de texto para expandirse horizontalmente y verticalmente
resultado_text.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")  # Ajustar al ancho y alto de la ventana

# Scrollbar para el texto
scrollbar = tk.Scrollbar(resultado_frame, orient="vertical", command=resultado_text.yview)
scrollbar.grid(row=2, column=1, sticky="ns")
resultado_text.config(yscrollcommand=scrollbar.set)

root.mainloop()