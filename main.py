import tkinter as tk
from tkinter import filedialog
import os
import shutil
from datetime import datetime
from tkinter import ttk

selected_origin_directory = ""
selected_destination_directory = ""
image_list_path = ""
num_imagenes = 0

# Método para seleccionar el directorio de origen
def select_origin_directory():
    global selected_origin_directory
    selected_origin_directory = filedialog.askdirectory()
    if selected_origin_directory:
        origin_label.config(text=f"Directorio de origen: {selected_origin_directory}")
        image_list_path = os.path.join(selected_origin_directory, "image_list.txt")
        count_images(selected_origin_directory, image_list_path)
        update_image_count()

# Método para seleccionar el directorio de destino
def select_destination_directory():
    global selected_destination_directory
    selected_destination_directory = filedialog.askdirectory()
    if selected_destination_directory:
        destination_label.config(text=f"Directorio de destino: {selected_destination_directory}")
        if selected_origin_directory:
            enable_organize_button()  # Habilitar el botón ORGANIZAR

# Método para contar el número de imágenes en un directorio y generar la lista
def count_images(directory, image_list_path):
    global num_imagenes
    with open(image_list_path, "w", encoding="utf-8") as image_list:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    num_imagenes += 1
                    image_path = os.path.join(root, file)
                    image_list.write(image_path + "\n")

# Método para actualizar el conteo de imágenes
def update_image_count():
    origin_label.config(text=f"Directorio de origen: {selected_origin_directory}")
    num_images_label.config(text=f"Nº de imágenes: {num_imagenes}")

# Método para habilitar el botón "ORGANIZAR"
def enable_organize_button():
    organize_button.config(state="active")

# Método para organizar las imágenes (genera acciones.txt)
def organize_images():
    if selected_origin_directory and selected_destination_directory:
        actions_file = os.path.join(selected_origin_directory, "acciones.txt")
        with open(actions_file, "w", encoding="utf-8") as actions:
            for root, dirs, files in os.walk(selected_origin_directory):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                        file_path = os.path.join(root, file)
                        file_path = os.path.normpath(file_path)  # Normalizar el separador de ruta
                        timestamp = get_image_timestamp(file_path)
                        destination_folder = create_destination_folder(timestamp)
                        new_file_name = f"{timestamp.strftime('%Y-%m-%d_%H_%M_%S')}.jpg"  # Nuevo nombre en formato YYYY-MM-DD_HH_MI_SS.jpg
                        new_file_path = os.path.normpath(os.path.join(destination_folder, new_file_name))  # Normalizar el separador de ruta
                        actions.write(f"{file_path} -> {new_file_path}\n")
        
        # Llamamos a la función para copiar imágenes y mostrar la barra de progreso
        # De momento queda comentado hasta que el código esté más depurado
        # copy_images(actions_file)

# Método para obtener la marca de tiempo de la imagen
def get_image_timestamp(image_path):
    timestamp = os.path.getctime(image_path)
    return datetime.fromtimestamp(timestamp)

# Método para copiar imágenes y mostrar la barra de progreso
def copy_images(actions_file):
    with open(actions_file, "r", encoding="utf-8") as actions:
        action_lines = actions.readlines()
    
    total_actions = len(action_lines)
    progress_bar["maximum"] = total_actions
    progress = 0
    
    for action in action_lines:
        source, destination = action.strip().split(" -> ")
        source = os.path.normpath(source)  # Normalizar el separador de ruta
        destination = os.path.normpath(destination)  # Normalizar el separador de ruta
        shutil.copy(source, destination)  # Copiar la imagen
        progress += 1
        progress_bar["value"] = progress
        root.update_idletasks()  # Actualizar la barra de progreso

# Método para crear el nombre de la carpeta de destino
def create_destination_folder(timestamp):
    timestamp_str = timestamp.strftime('%Y%m%d')
    return os.path.join(selected_destination_directory, f"{timestamp_str} - XXXX")

root = tk.Tk()
root.title("Organizador de Fotos")

# Configuración del fondo gris
root.configure(bg="gray")

# Crear una etiqueta para el título
title_label = tk.Label(root, text="Paso 1: Origen", font=("Helvetica", 16), bg="gray")
title_label.pack(pady=10)

# Botón para seleccionar el directorio de origen
select_origin_button = tk.Button(root, text="Seleccionar Directorio de Origen", command=select_origin_directory)
select_origin_button.pack()

# Etiqueta para mostrar el directorio de origen
origin_label = tk.Label(root, text="", bg="gray")
origin_label.pack()

# Etiqueta para mostrar el número de imágenes origen
num_images_label = tk.Label(root, text="", bg="gray")
num_images_label.pack()

# Botón para seleccionar el directorio de destino
select_destination_button = tk.Button(root, text="Seleccionar Directorio de Destino", command=select_destination_directory)
select_destination_button.pack(pady=10)

# Etiqueta para mostrar el directorio de destino
destination_label = tk.Label(root, text="", bg="gray")
destination_label.pack()

# Botón para organizar imágenes (inicialmente deshabilitado)
organize_button = tk.Button(root, text="ORGANIZAR", state="disabled", command=organize_images)
organize_button.pack(pady=10)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
