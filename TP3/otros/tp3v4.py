import random
import tkinter as tk
from tkinter import ttk
import csv
import pandas as pd

def simulacion_monte_carlo(X, N, p_recuerdo, p_no_recuerdo, compra_recuerdo_si, compra_no_recuerdo_si):
    # Inicializamos acumuladores
    acum_compra_si_recuerda = 0
    acum_compra_no_recuerda = 0
    acum_compra_si = 0
    
    # Simulación de Monte Carlo
    for _ in range(N):
        # Generamos un individuo al azar
        recuerda = random.random() < p_recuerdo
        
        # Si el individuo recuerda el mensaje
        if recuerda:
            # Determinamos si compra el producto
            compra = random.random()
            if compra < compra_recuerdo_si:
                acum_compra_si_recuerda += 1
                acum_compra_si += 1
        else:
            # Determinamos si compra el producto
            compra = random.random()
            if compra < compra_no_recuerdo_si:
                acum_compra_no_recuerda += 1
                acum_compra_si += 1
    
    # Devolvemos los acumuladores
    return acum_compra_si_recuerda, acum_compra_no_recuerda, acum_compra_si

def guardar_datos_en_archivo(nombre_archivo, datos):
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Recuerda y SI compra", "No recuerda y SI compra", "Acumulador SI compra"])
        writer.writerows(datos)

def mostrar_datos_desde_archivo(nombre_archivo):
    df = pd.read_csv(nombre_archivo)
    return df

def mostrar_resultados(X, N, i, j, acum_compra_si_recuerda, acum_compra_no_recuerda, acum_compra_si):
    total_compra_si_recuerda = acum_compra_si_recuerda / N
    total_compra_no_recuerda = acum_compra_no_recuerda / N
    total_compra_si = acum_compra_si / N

    resultados = f"Resultados de la simulación:\n\n" \
                 f"Duración de la simulación en semanas (X): {X}\n" \
                 f"Cantidad total de filas simuladas (N): {N}\n" \
                 f"Número de iteraciones a mostrar (i): {i}\n" \
                 f"Hora de inicio para mostrar las iteraciones (j): {j}\n" \
                 f"Probabilidad general de compra definitivamente sí: {total_compra_si:.4f}\n"

    return resultados

def ejecutar_simulacion(X, N, i, j):
    p_recuerdo = 0.40
    p_no_recuerdo = 0.50
    compra_recuerdo_si = 0.40
    compra_no_recuerdo_si = 0.10

    acum_compra_si_recuerda, acum_compra_no_recuerda, acum_compra_si = simulacion_monte_carlo(X, N, p_recuerdo, p_no_recuerdo, compra_recuerdo_si, compra_no_recuerdo_si)
    resultados = mostrar_resultados(X, N, i, j, acum_compra_si_recuerda, acum_compra_no_recuerda, acum_compra_si)
    
    # Guardar los datos en un archivo CSV
    datos = [(acum_compra_si_recuerda, acum_compra_no_recuerda, acum_compra_si)]
    guardar_datos_en_archivo("datos_simulacion.csv", datos)
    
    return resultados

def mostrar_interfaz():
    root = tk.Tk()
    root.title("Simulación de Monte Carlo")

    def iniciar_simulacion():
        try:
            X = int(entrada_X.get())
            N = int(entrada_N.get())
            i = int(entrada_i.get())
            j = int(entrada_j.get())
            
            if X <= 0 or N <= 0 or i <= 0 or j <= 0:
                raise ValueError("Los valores de X, N, i y j deben ser mayores que cero.")
            
            resultados = ejecutar_simulacion(X, N, i, j)

            etiqueta_resultados.config(text=resultados)
            
            # Mostrar los datos en una tabla
            df = mostrar_datos_desde_archivo("datos_simulacion.csv")
            ventana_datos = tk.Toplevel(root)
            ventana_datos.title("Datos de la simulación")
            tabla = ttk.Treeview(ventana_datos)
            tabla["columns"] = list(df.columns)
            tabla.heading("#0", text="Índice")
            for col in df.columns:
                tabla.heading(col, text=col)
            for i, row in df.iterrows():
                tabla.insert("", tk.END, text=i, values=list(row))
            tabla.pack()
            
            # Mostrar la fila N
            fila_n = df.iloc[-1]
            etiqueta_fila_n.config(text=f"Fila N: {list(fila_n)}")
        
        except ValueError as error:
            etiqueta_resultados.config(text=str(error))

    etiqueta_X = ttk.Label(root, text="Duración de la simulación en semanas (X):")
    etiqueta_X.grid(row=0, column=0, padx=5, pady=5)
    entrada_X = ttk.Entry(root)
    entrada_X.grid(row=0, column=1, padx=5, pady=5)

    etiqueta_N = ttk.Label(root, text="Cantidad total de filas a simular (N):")
    etiqueta_N.grid(row=1, column=0, padx=5, pady=5)
    entrada_N = ttk.Entry(root)
    entrada_N.grid(row=1, column=1, padx=5, pady=5)

    etiqueta_i = ttk.Label(root, text="Número de iteraciones a mostrar (i):")
    etiqueta_i.grid(row=2, column=0, padx=5, pady=5)
    entrada_i = ttk.Entry(root)
    entrada_i.grid(row=2, column=1, padx=5, pady=5)

    etiqueta_j = ttk.Label(root, text="Hora de inicio para mostrar las iteraciones (j):")
    etiqueta_j.grid(row=3, column=0, padx=5, pady=5)
    entrada_j = ttk.Entry(root)
    entrada_j.grid(row=3, column=1, padx=5, pady=5)

    boton_simular = ttk.Button(root, text="Simular", command=iniciar_simulacion)
    boton_simular.grid(row=4, columnspan=2, padx=5, pady=5)

    etiqueta_resultados = ttk.Label(root, text="")
    etiqueta_resultados.grid(row=5, columnspan=2, padx=5, pady=5)
    
    etiqueta_fila_n = ttk.Label(root, text="")
    etiqueta_fila_n.grid(row=6, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    mostrar_interfaz()
