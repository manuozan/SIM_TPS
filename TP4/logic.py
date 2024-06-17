import tkinter as tk
from tkinter import ttk
import json

def create_table(root):
    headers = [
        'Evento', 'Reloj [min]', 'RND tiempo', 'Tiempo entre \n llegadas', 
        'Próxima llegada', 'RND Tipo', 'Tipo', 'RND', 
        'Tiempo estacionado', 'fin_cobro', '1', '2', '3', '4', '5', '6', '7', '8', 'Estado cobro', 'Cola cobro', 'Ganancia', 'Ganancia AC', 'Cant L Ocupados', 'Ac Tiempo espera'
    ]

    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview', 
                    background='#333333', 
                    foreground='white', 
                    rowheight=25, 
                    fieldbackground='#333333')
    style.map('Treeview', 
              background=[('selected', '#666666')])
    style.configure('Treeview.Heading', 
                    background='#444444', 
                    foreground='white',
                    font=('Helvetica', 8, 'bold'))

    tree = ttk.Treeview(frame, columns=headers, show='headings', style='Treeview')
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=110, anchor=tk.CENTER)
    
    data = [
        ('Inicialización', '0', '0.51', '9.27', '9.27', '', '', '', '', '', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', '0', '0', '0', '0', '0'),
        ('llegada_auto (1)', '9.27', '0.28', '4.27', '13.54', '0.36', 'pequeño', '0.62', '120', '129.27', '1 - 129.27', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Libre', 'Ocupado', '0', '0', '0', '1', '0'),
    ]
    """with open('estado_simulacion.json') as estado: 
        data = json.load(estado, ensure_ascii=False, indent=4)"""
    
    
    

    
    for row in data:
        tree.insert('', 'end', values=row)
    
    scrollbar_v = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    scrollbar_h = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
    tree.configure(yscroll=scrollbar_v.set, xscroll=scrollbar_h.set)
    
    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar_v.grid(row=0, column=1, sticky='ns')
    scrollbar_h.grid(row=1, column=0, sticky='ew')
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    return tree

def open_table():    
    table_window = tk.Toplevel()
    table_window.title('Tabla con Scrollbars')
    table_window.state('zoomed')
    create_table(table_window)

