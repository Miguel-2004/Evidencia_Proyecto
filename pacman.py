# Importa la función `choice` para seleccionar un elemento aleatorio y las funciones necesarias de turtle
from random import choice
from turtle import *
# Importa las funciones `floor` y `vector` desde la librería 'freegames'
from freegames import floor, vector

# Se define el estado del juego, que incluye la puntuación actual
state = {'score': 0}

# Se crean dos objetos Turtle, uno para dibujar el camino (`path`) y otro para mostrar el puntaje (`writer`)
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

# Se define el mapa del juego con un arreglo de 1s, 0s y 2s. Los 1 representan caminos transitables, 
# los 0 son paredes, y los 2 son los puntos que Pac-Man puede comer.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
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

# Función para dibujar un cuadrado en las coordenadas (x, y) usando el objeto path
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)  # Moverse a las coordenadas (x, y)
    path.down()
    path.begin_fill()  # Comienza a llenar el cuadrado

    for count in range(4):
        path.forward(20)  # Avanza 20 unidades
        path.left(90)     # Gira 90 grados

    path.end_fill()  # Termina de llenar el cuadrado

# Función para obtener el índice de una posición en el mapa
def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20  # Redondea y escala la coordenada x
    y = (180 - floor(point.y, 20)) / 20   # Redondea y escala la coordenada y
    index = int(x + y * 20)  # Calcula el índice de la posición en la lista de tiles
    return index

# Función para comprobar si un punto es válido en el mapa
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:  # Si la posición es una pared (0), no es válida
        return False

    index = offset(point + 19)  # Comprobamos el borde derecho de la celda

    if tiles[index] == 0:  # Si la posición es una pared (0), no es válida
        return False

    return point.x % 20 == 0 or point.y % 20 == 0  # Asegura que el punto esté alineado en la cuadrícula

# Función para dibujar el mundo (mapa de juego)
def world():
    "Draw world using path."
    bgcolor('black')  # Fondo negro
    path.color('blue')  # Color azul para el camino

    for index in range(len(tiles)):  # Itera sobre cada tile del mapa
        tile = tiles[index]  # Obtiene el valor del tile (1 = camino, 0 = pared)

        if tile > 0:  # Si el tile es un camino
            x = (index % 20) * 20 - 200  # Calcula la posición x del tile
            y = 180 - (index // 20) * 20  # Calcula la posición y del tile
            square(x, y)  # Dibuja el cuadrado

            if tile == 1:  # Si el tile es un camino (1)
                path.up()
                path.goto(x + 10, y + 10)  # Posiciona el puntero en el centro del tile
                path.dot(2, 'white')  # Dibuja un punto blanco en el centro del tile

# Función para mover a Pac-Man y los fantasmas
def move():
    "Move pacman and all ghosts."
    writer.undo()  # Elimina el puntaje actual
    writer.write(state['score'])  # Muestra el puntaje actualizado

    clear()  # Borra la pantalla

    # Mueve a Pac-Man si la dirección es válida
    if valid(pacman + aim):
        pacman.move(aim)

    # Obtiene el índice del tile en el que se encuentra Pac-Man
    index = offset(pacman)

    # Si el tile es un punto (1), lo marca como comido (2) y aumenta la puntuación
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1  # Aumenta el puntaje
        x = (index % 20) * 20 - 200  # Calcula la posición x del tile
        y = 180 - (index // 20) * 20  # Calcula la posición y del tile
        square(x, y)  # Redibuja el cuadrado

    # Dibuja a Pac-Man en la nueva posición
    up()
    goto(pacman.x + 10, pacman.y + 10)  # Posición de Pac-Man
    dot(20, 'yellow')  # Dibuja el círculo de Pac-Man

    # Mueve a los fantasmas
    for point, course in ghosts:
        if valid(point + course):  # Si la siguiente posición del fantasma es válida
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]  # Opciones de movimiento para el fantasma
            plan = choice(options)  # Elige un movimiento aleatorio
            course.x = plan.x
            course.y = plan.y

        # Dibuja el fantasma en la nueva posición
        up()
        goto(point.x + 10, point.y + 10)  # Posición del fantasma
        dot(20, 'red')  # Dibuja el círculo del fantasma en rojo

    update()  # Actualiza la pantalla

    # Verifica si Pac-Man ha chocado con algún fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:  # Si Pac-Man está cerca de un fantasma
            return  # Fin del juego si Pac-Man choca con un fantasma

    # Llama a la función 'move' cada 100 milisegundos para seguir el juego
    ontimer(move, 100)

# Función para cambiar la dirección de Pac-Man
def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):  # Si el movimiento es válido
        aim.x = x
        aim.y = y  # Cambia la dirección de Pac-Man

# Configura la ventana de juego
setup(420, 420, 370, 0)  # Tamaño de la ventana
hideturtle()  # Oculta el cursor de la tortuga
tracer(False)  # Desactiva el trazado para mejorar el rendimiento
writer.goto(160, 160)  # Posición del puntaje
writer.color('white')  # Color del texto
writer.write(state['score'])  # Muestra el puntaje inicial
listen()  # Activa el escuchar las teclas
onkey(lambda: change(5, 0), 'Right')  # Movimiento hacia la derecha
onkey(lambda: change(-5, 0), 'Left')  # Movimiento hacia la izquierda
onkey(lambda: change(0, 5), 'Up')  # Movimiento hacia arriba
onkey(lambda: change(0, -5), 'Down')  # Movimiento hacia abajo
world()  # Dibuja el mapa
move()  # Inicia el movimiento
done()  # Finaliza el juego
