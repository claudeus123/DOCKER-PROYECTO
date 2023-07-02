from datetime import date, timedelta
import cv2
import psycopg2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox
import re

def conection():
    conn = psycopg2.connect(
        host="babar.db.elephantsql.com",
        port=5432,
        database="oqrbjeeo",
        user="oqrbjeeo",
        password="zCL8pGLtlSQwJl2eMLu5OlaTDMwuc4zL"
    )
    print("Conexion realizada")
    return conn


def leer_codigo_qr(url):
    # Crear un objeto VideoCapture para la transmisión de video
    cap = cv2.VideoCapture(url)

    while True:
        # Capturar el fotograma actual de la transmisión
        ret, frame = cap.read()

        # Convertir el fotograma a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los códigos QR en el fotograma
        codigos_qr = pyzbar.decode(gray)

        # Recorrer los códigos QR encontrados
        for codigo in codigos_qr:
            # Extraer el contenido del código QR
            contenido = codigo.data.decode("utf-8")

            # Imprimir el resultado por consola
            print("Código QR encontrado:", contenido)
            cv2.imshow("Lector de código QR", frame)
            cap.release()
            cv2.destroyAllWindows()
            return contenido


def agregar_cliente():
    # Crear una ventana de Tkinter
    ventana = tk.Tk()
    ventana.title("Agregar Cliente")

    # Etiquetas y campos de entrada para los atributos del cliente
    tk.Label(ventana, text="Nombre del cliente:").pack()
    client_name_entry = tk.Entry(ventana)
    client_name_entry.pack()

    tk.Label(ventana, text="Apellido del cliente:").pack()
    last_name_entry = tk.Entry(ventana)
    last_name_entry.pack()

    tk.Label(ventana, text="Edad del cliente:").pack()
    client_age_entry = tk.Entry(ventana)
    client_age_entry.pack()
    
    tk.Label(ventana, text="Email del cliente:").pack()
    email_entry = tk.Entry(ventana)
    email_entry.pack()

    def agregar_cliente_click():
        # Obtener los valores ingresados por el usuario
        client_name = client_name_entry.get()
        last_name = last_name_entry.get()
        client_age = client_age_entry.get()
        validity = True
        email = email_entry.get()

        # Validar que se ingresen todos los valores requeridos
        if not client_name or not last_name or not client_age or not validity or not email:
            messagebox.showerror("Error", "Por favor, ingresa todos los valores requeridos.")
            return

        # Conectarse a la base de datos PostgreSQL
        conexion = conection()

        url = "http://192.168.198.228:8080/video"

        # Generar el código QR leyéndolo desde el teléfono
        code = leer_codigo_qr(url)
        
        pattern = r"RUN=(\d{7,8}-([0-9]|[K]))"

        result = re.search(pattern, code)
        
        if result is None:
            messagebox.showerror("Error", "El codigo QR ingresado no es válido")
            return
        else:  
            id_number = result.group(1)
        
        if code is None:
            messagebox.showerror("Error", "No se pudo leer el código QR desde el teléfono")
            return

        # Crear el cursor para ejecutar las consultas SQL
        cursor = conexion.cursor()

        # Insertar el nuevo cliente en la base de datos

        # Obtener la fecha actual
        fecha_actual = date.today()
        # Calcular la fecha de finalización (30 días después de la fecha actual)
        fecha_finalizacion = fecha_actual + timedelta(days=30)

        cursor.execute("""
            INSERT INTO client (client_name, last_name, id_number, client_age, validity, email, code, date_init, date_end)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (client_name, last_name, id_number, client_age, validity, email, code, fecha_actual, fecha_finalizacion))

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Cliente agregado", "Cliente agregado correctamente")

    # Botón para agregar cliente
    agregar_button = tk.Button(ventana, text="Agregar Cliente", command=agregar_cliente_click)
    agregar_button.pack()

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()

agregar_cliente()