import tkinter as tk
from Join import *
import serial

# Establecer la conexión con la base de datos

conn = connect()
url = "http://192.168.186.197:8080/video"
arduino = serial.Serial('/dev/tty', 9600, timeout=10)
arduino.flushInput()
print(arduino)

# Función para ejecutar al presionar el botón
def ingresar_cliente():
    mensaje_label.configure(text="Buscando cliente")
    resultado = get_cliente_por_code(conn, url, arduino)
    print(resultado)
    mensaje_label.configure(text=resultado)


# Crear la ventana
ventana = tk.Tk()
ventana.title("Ingresar Cliente")

# Crear un botón
boton = tk.Button(ventana, text="Ingresar", command=ingresar_cliente)
boton.pack()

# Crear una etiqueta para mostrar el mensaje
mensaje_label = tk.Label(ventana, text="")
mensaje_label.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()