import base64
import io
import os
import threading
import time
from PIL import Image
import curses

# Función para rotar la imagen
def rotar_imagen(imagen, direccion, angulo_rotacion):
    angulo_rotacion += 10 if direccion == 'izquierda' else -10
    return imagen.rotate(angulo_rotacion), angulo_rotacion

def map_pixels_to_ascii(image):
    ascii_str = ''
    for pixel_value in image.getdata():
        ascii_str += ' .:-=+*#%&@'[pixel_value // 25]
    return ascii_str

# In your mostrar_imagen function
def mostrar_imagen(stdscr, imagen_rotada):
    try:
        stdscr.clear()
        stdscr.addstr(0, 0, "Presiona 'q' para salir")
        stdscr.addstr(0, 25, "Presiona 'd' para rotar a la derecha.")
        stdscr.addstr(0, 65, "Presiona 'i' para rotar a la izquierda.")
        imagen_renderizada = imagen_rotada.resize((stdscr.getmaxyx()[1] - 2, stdscr.getmaxyx()[0] - 2))
        imagen_renderizada_ascii = map_pixels_to_ascii(imagen_renderizada.convert('L'))
        stdscr.addstr(1, 0, imagen_renderizada_ascii)
        stdscr.refresh()
        time.sleep(0.1)
    except KeyboardInterrupt:
        return

# Función principal
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Cargando imagen...")
    stdscr.refresh()

    # Cargamos la imagen
    with open("motor.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    imagen = Image.open(io.BytesIO(base64.b64decode(encoded_string)))

    angulo_rotacion = 0
    direccion = 'derecha'
    stdscr.nodelay(True)  # make getch non-blocking

    # Display instructions
    stdscr.addstr(1, 0, "Instrucciones:")
    stdscr.addstr(2, 0, "Presiona 'd' para rotar a la derecha.")
    stdscr.addstr(3, 0, "Presiona 'i' para rotar a la izquierda.")
    stdscr.addstr(4, 0, "Presiona 'q' para salir.")
    stdscr.refresh()

    while True:
        try:
            # Check for user input
            key = stdscr.getch()
            if key == ord('d'):
                direccion = 'derecha'
            elif key == ord('i'):
                direccion = 'izquierda'
            elif key == ord('q'):
                break

            # Rotamos la imagen
            imagen_rotada, angulo_rotacion = rotar_imagen(imagen, direccion, angulo_rotacion)

            # Mostramos la imagen en la terminal
            mostrar_imagen(stdscr, imagen_rotada)

            time.sleep(0.1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    curses.wrapper(main)