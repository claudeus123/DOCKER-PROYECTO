import cv2
import psycopg2
from datetime import datetime, date
from pyzbar import pyzbar
import serial 

# Establecer la conexión con la base de datos
def connect():
    conn = psycopg2.connect(
        host="babar.db.elephantsql.com",
        port=5432,
        database="oqrbjeeo",
        user="oqrbjeeo",
        password="zCL8pGLtlSQwJl2eMLu5OlaTDMwuc4zL"
    )
    print("Conexión realizada")
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

        # Mostrar el fotograma en una ventana




def get_cliente_por_code(conn,url,arduino):
    
    thisarduino=arduino
    code = leer_codigo_qr(url)
    cur = conn.cursor()

    # Ejecutar la consulta con el parámetro rut
    cur.execute("SELECT * FROM client WHERE code = %s", (code,))
    cliente = cur.fetchone()
    

    # Cerrar el cursor
    cur.close()

    if cliente:
        return comprobar_validez(cliente,thisarduino)
    else:
        
        return "Usuario no encontrado", thisarduino.write(b'\n4')
    


def comprobar_validez(cliente,arduino):

    thisarduino=arduino
    fecha_actual = date.today()


    fecha_init_str = str(cliente[7])
    fecha_end_str = str(cliente[8])

    fecha_init = datetime.strptime(fecha_init_str, '%Y-%m-%d').date()
    fecha_end = datetime.strptime(fecha_end_str, '%Y-%m-%d').date()
   
    if fecha_init <= fecha_actual <= fecha_end:
        
        return "Usuario valido", thisarduino.write(b'\n6')
    else:
        
        return "Usuario no valido", thisarduino.write(b'5')
    
