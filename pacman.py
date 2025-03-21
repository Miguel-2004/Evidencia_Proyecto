# Para asegurarnos de que el código cumpla con las reglas de estilo PEP8, 
# se realizarán los siguientes cambios:
# 
# 1. Líneas demasiado largas: Las líneas de código deben ser de un máximo de 79 caracteres.
# 2. Espacios en blanco: Se deben colocar correctamente los espacios en blanco alrededor de operadores y después de las comas.
# 3. Nombres de funciones y variables: Los nombres de las funciones y variables deben estar en minúsculas con guiones bajos para separar las palabras.
# 4. Comentarios: Los comentarios deben estar bien formateados y ser descriptivos.

# Importa la función `choice` para seleccionar un elemento aleatorio
# y las funciones necesarias de turtle
from random import choice
from turtle import *
# Importa las funciones `floor` y `vector` desde la librería 'freegames'
from freegames import floor, vector

# Se define el estado del juego, que incluye la puntuación actual
state = {'score': 0}

# Se crean dos objetos Turtle, uno para dibujar el camino (`path`)
# y otro para mostrar el puntaje (`writer`)
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Se define la dirección de movimiento de Pac-Man
aim = vector(5, 0)
# Se define la posición inicial de Pac-Man
pacman = vector(-40, -80)

# Se definen los fantasmas, cada uno con una posición y una dirección de movimiento
ghosts = [
    [vector(-180, 160), vector(5, 0)],  # Fantasma 1
    [vector(-180, -160), vector(0, 5)],  # Fantasma 2
    [vector(100, 160), vector(0, -5)],   # Fantasma 3
    [vector(100, -160), vector(-5, 0)],  # Fantasma 4
]

# Se define el mapa del juego con un arreglo de 1s, 0s y 2s.
# Los 1 representan caminos transitables, los 0 son paredes,
# y los 2 son los puntos que Pac-Man puede comer.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# Función para dibujar un círculo como el alimento
def food(x, y):
    """Draw food using path at (x, y)."""
    path.up()
    path.goto(x, y)  # Moverse a las coordenadas (x, y)
    path.down()
    path.color("yellow")  # Color amarillo para el alimento
    path.begin_fill()  # Comienza a llenar el círculo
    path.circle(5)  # Dibuja un círculo con radio 5
    path.end_fill()  # Termina de llenar el círculo

# Función para obtener el índice de una posición en el mapa
def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20  # Redondea y escala la coordenada x
    y = (180 - floor(point.y, 20)) / 20   # Redondea y escala la coordenada y
    index = int(x + y * 20)  # Calcula el índice de la posición en la lista de tiles
    return index

# Función para comprobar si un punto es válido en el mapa
def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:  # Si la posición es una pared (0), no es válida
        return False

    index = offset(point + 19)  # Comprobamos el borde derecho de la celda

    if tiles[index] == 0:  # Si la posición es una pared (0), no es válida
        return False

    return point.x % 20 == 0 or point.y % 20 == 0  # Asegura que el punto esté alineado en la cuadrícula

# Función para dibujar el mundo (mapa de juego)
def world():
    """Draw world using path."""
    bgcolor('black')  # Fondo negro
    path.color('blue')  # Color azul para el camino

    for index in range(len(tiles)):  # Itera sobre cada tile del mapa
        tile = tiles[index]  # Obtiene el valor del tile (1 = camino, 0 = pared)

        if tile == 2:  # Si el tile es un punto comestible
            x = (index % 20) * 20 - 200  # Calcula la posición x del tile
            y = 180 - (index // 20) * 20  # Calcula la posición y del tile
            food(x, y)  # Dibuja el círculo (alimento)

        if tile > 0:  # Si el tile es un camino
            x = (index % 20) * 20 - 200  # Calcula la posición x del tile
            y = 180 - (index // 20) * 20  # Calcula la posición y del tile
            path.up()
            path.goto(x, y)  # Moverse a las coordenadas (x, y)
            path.down()
            path.begin_fill()  # Comienza a llenar el camino
            for _ in range(4):  # Dibuja un cuadrado de 20x20
                path.forward(20)
                path.left(90)
            path.end_fill()  # Termina de llenar el cuadrado

# Función principal que inicia el juego
def main():
    """Run Pac-Man."""
    setup(420, 420, 370, 0)  # Configura la ventana de juego
    tracer(False)  # Desactiva la animación para optimizar
    world()  # Dibuja el mundo (mapa)
    tracer(True)  # Vuelve a activar la animación
    done()  # Finaliza el juego

# Inicia el juego llamando a la función principal
main()
