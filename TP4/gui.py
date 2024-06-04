import tkinter as tk
from tkinter import ttk
from logic import open_table

root = tk.Tk()
root.title('TP4')
root.resizable(False, False)
# Ajustar el tamaño de la ventana
root.geometry('200x560') 
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


# Frame para el título con la imagen
frame_titulo = ttk.Frame(root, padding=(10, 10))
frame_titulo.grid(row=0, column=0, columnspan=2, sticky='ew')

# Etiqueta para el título
title_label = ttk.Label(frame_titulo, text="Playa de estacionamiento", font=('Helvetica', 10, 'bold'))
title_label.grid(row=0, column=1, padx=10)

# Frame "Indice de llegadas"
frame_llegadas = ttk.LabelFrame(root, padding=(10, 10), borderwidth=2, text='Indice de llegadas')
frame_llegadas.grid(row=1, column=0, sticky='ew', columnspan=2)
frame_llegadas.grid_columnconfigure(0, weight=1)
frame_llegadas.grid_columnconfigure(1, weight=1)

lbl_indice_llegadas = ttk.Label(frame_llegadas, text='Tiempo:')
lbl_indice_llegadas.grid(row=1, column=0, sticky='ew')
entry_indice_llegadas = ttk.Entry(frame_llegadas, width=10)
entry_indice_llegadas.grid(row=1, column=1, sticky='ew')

# Frame "Tipo de automovil"
frame_automovil = ttk.LabelFrame(root, padding=(10, 10), borderwidth=2, text='Tipo de automóvil')
frame_automovil.grid(row=2, column=0, sticky='ew', columnspan=2)
frame_automovil.grid_columnconfigure(0, weight=1)
frame_automovil.grid_columnconfigure(1, weight=1)

lbl_pequenos = ttk.Label(frame_automovil, text='Pequeños:')
lbl_pequenos.grid(row=1, column=0, sticky='ew')
entry_pequenos = ttk.Entry(frame_automovil, width=10)
entry_pequenos.grid(row=1, column=1, sticky='ew')

lbl_grandes = ttk.Label(frame_automovil, text='Grandes:')
lbl_grandes.grid(row=2, column=0, sticky='ew')
entry_grandes = ttk.Entry(frame_automovil, width=10)
entry_grandes.grid(row=2, column=1, sticky='ew')

lbl_utilitario = ttk.Label(frame_automovil, text='Utilitario:')
lbl_utilitario.grid(row=3, column=0, sticky='ew')
entry_utilitario = ttk.Entry(frame_automovil, width=10)
entry_utilitario.grid(row=3, column=1, sticky='ew')

# Frame "Tiempo de estacionamiento"
frame_estacionamiento = ttk.LabelFrame(root, padding=(10, 10), borderwidth=2, text='Tiempo de estacionamiento')
frame_estacionamiento.grid(row=3, column=0, sticky='ew', columnspan=2)
frame_estacionamiento.grid_columnconfigure(0, weight=1)
frame_estacionamiento.grid_columnconfigure(1, weight=1)

lbl_hora1 = ttk.Label(frame_estacionamiento, text='1 hora:')
lbl_hora1.grid(row=1, column=0, sticky='ew')
entry_hora1 = ttk.Entry(frame_estacionamiento, width=10)
entry_hora1.grid(row=1, column=1, sticky='ew')

lbl_hora2 = ttk.Label(frame_estacionamiento, text='2 horas:')
lbl_hora2.grid(row=2, column=0, sticky='ew')
entry_hora2 = ttk.Entry(frame_estacionamiento, width=10)
entry_hora2.grid(row=2, column=1, sticky='ew')

lbl_hora3 = ttk.Label(frame_estacionamiento, text='3 horas:')
lbl_hora3.grid(row=3, column=0, sticky='ew')
entry_hora3 = ttk.Entry(frame_estacionamiento, width=10)
entry_hora3.grid(row=3, column=1, sticky='ew')

lbl_hora4 = ttk.Label(frame_estacionamiento, text='4 horas:')
lbl_hora4.grid(row=4, column=0, sticky='ew')
entry_hora4 = ttk.Entry(frame_estacionamiento, width=10)
entry_hora4.grid(row=4, column=1, sticky='ew')

# Frame "Tiempo de cobro"
frame_cobro = ttk.LabelFrame(root, padding=(10, 10), borderwidth=2, text='Tiempo de cobro')
frame_cobro.grid(row=4, column=0, sticky='ew', columnspan=2)
frame_cobro.grid_columnconfigure(0, weight=1)
frame_cobro.grid_columnconfigure(1, weight=1)

lbl_tiempo_cobro = ttk.Label(frame_cobro, text='Tiempo:')
lbl_tiempo_cobro.grid(row=1, column=0, sticky='ew')
entry_tiempo_cobro = ttk.Entry(frame_cobro, width=10)
entry_tiempo_cobro.grid(row=1, column=1, sticky='ew')

# Frame "Filtrar"
frame_filtrar = ttk.LabelFrame(root, text='Filtrar', padding=(10, 10))
frame_filtrar.grid(row=5, column=0, columnspan=2, sticky='ew')
frame_filtrar.grid_columnconfigure(0, weight=1)
frame_filtrar.grid_columnconfigure(1, weight=1)

# Combobox para filtrar
filter_combobox = ttk.Combobox(frame_filtrar, values=['No filtrar','Filtrar por iteraciones', 'Filtrar por hora'], state='readonly')
filter_combobox.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# Labels y entries
labels = ['Inicio', 'Fin']
for i, label_text in enumerate(labels, start=1):
    label = ttk.Label(frame_filtrar, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
    entry = ttk.Entry(frame_filtrar)
    entry.grid(row=i, column=1, sticky='ew')


# Botón "Iniciar simulación"
btn_iniciar_simulacion = ttk.Button(root, text='Iniciar simulación', command=open_table)
btn_iniciar_simulacion.grid(row=6, column=0, pady=10, columnspan=2, sticky='ew')


def set_default_values():
    # Valores predefinidos
    entry_indice_llegadas.insert(0, '13')

    entry_pequenos.insert(0, '45')
    entry_grandes.insert(0, '25')
    entry_utilitario.insert(0, '30')

    entry_hora1.insert(0, '50')
    entry_hora2.insert(0, '30')
    entry_hora3.insert(0, '15')
    entry_hora4.insert(0, '5')
    entry_tiempo_cobro.insert(0, '2')
    filter_combobox.set('No filtrar')
    
set_default_values()
root.mainloop()
