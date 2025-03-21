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

# Función para dibujar un cuadrado en las coordenadas (x, y) usando el objeto path
def square(x, y):
    """Draw square using path at (x, y)."""
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

        if tile > 0:  # Si el tile es un camino
            x = (index % 20) * 20 - 200  # Calcula la posición x del tile
            y = 180 - (index // 20) * 20  # Calcula la posición y del tile
            square(x, y)  # Dibuja el cuadrado en la posición correspondiente

# Función para mover Pac-Man en la dirección deseada
def move():
    """Move pacman in the direction of aim."""
    pacman.move(aim)  # Mueve Pac-Man en la dirección de 'aim'

    if not valid(pacman):  # Si la nueva posición de Pac-Man no es válida
        pacman.move(-aim)  # Retrocede Pac-Man al lugar anterior

# Función para controlar las teclas de dirección
def change(x, y):
    """Change pacman aim to x, y."""
    aim.x = x
    aim.y = y

# Función para verificar si Pac-Man ha comido un punto
def eat():
    """Eat point if pacman is on a point."""
    index = offset(pacman)  # Obtiene el índice de la posición de Pac-Man
    if tiles[index] == 2:  # Si el tile es un punto (2)
        tiles[index] = 1  # Cambia el tile a camino (1)
        state['score'] += 10  # Aumenta la puntuación

# Función para verificar si un fantasma ha atrapado a Pac-Man
def collide():
    """Check if pacman collides with any ghost."""
    for ghost in ghosts:
        if pacman.distance(ghost[0]) < 20:  # Si Pac-Man está demasiado cerca de un fantasma
            return True
    return False

# Función principal que se ejecuta en un bucle continuo
def game():
    """Run the game loop."""
    move()  # Mueve Pac-Man
    eat()  # Verifica si Pac-Man ha comido un punto

    if collide():  # Si Pac-Man choca con un fantasma
        print(f"Game Over. Score: {state['score']}")  # Muestra el puntaje final
        return  # Termina el juego

    writer.clear()  # Limpia el puntaje anterior
    writer.write(f"Score: {state['score']}", align='center', font=('Courier', 16, 'normal'))  # Muestra el puntaje actualizado

    update()  # Actualiza la pantalla
    ontimer(game, 100)  # Ejecuta el juego nuevamente después de 100 milisegundos

# Inicia el juego
setup(420, 420, 370, 0)  # Configura la ventana del juego
hideturtle()  # Oculta el puntero de la tortuga
tracer(0)  # Desactiva la animación automática
world()  # Dibuja el mundo
writer.goto(0, 160)  # Coloca el escritor en la parte superior
writer.color('white')  # Define el color blanco para el texto
writer.write(f"Score: {state['score']}", align='center', font=('Courier', 16, 'normal'))  # Muestra el puntaje inicial
listen()  # Escucha los eventos de teclado
onkey(lambda: change(5, 0), 'Right')  # Mueve Pac-Man a la derecha
onkey(lambda: change(-5, 0), 'Left')  # Mueve Pac-Man a la izquierda
onkey(lambda: change(0, 5), 'Up')  # Mueve Pac-Man hacia arriba
onkey(lambda: change(0, -5), 'Down')  # Mueve Pac-Man hacia abajo

# Ejecuta el bucle principal del juego
game()
done()
