from random import choice  # Importa la función choice para seleccionar aleatoriamente entre opciones
from turtle import *  # Importa todas las funciones del módulo turtle para gráficos
from freegames import floor, vector  # Importa las funciones floor y vector desde freegames

state = {'score': 0}  # Define un diccionario que contiene la puntuación del juego
path = Turtle(visible=False)  # Crea un objeto Turtle que será usado para dibujar el mapa
writer = Turtle(visible=False)  # Crea otro Turtle para escribir el puntaje
aim = vector(5, 0)  # Establece la dirección inicial del movimiento de Pacman (a la derecha)
pacman = vector(-40, -80)  # Establece la posición inicial de Pacman
ghosts = [  # Define una lista de fantasmas, cada uno tiene una posición y una dirección
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

tiles = [  # Representa el mapa del juego en una lista de ceros (vacío), unos (camino) y dos (comida)
    # ... Aquí está la representación completa del mapa ...
]

def square(x, y):  # Función para dibujar un cuadrado en las coordenadas (x, y)
    path.up()  # Levanta el lápiz para moverlo sin dibujar
    path.goto(x, y)  # Mueve el lápiz a la posición (x, y)
    path.down()  # Baja el lápiz para empezar a dibujar
    path.begin_fill()  # Inicia el relleno del cuadrado

    for count in range(4):  # Dibuja un cuadrado de 4 lados
        path.forward(20)  # Avanza 20 unidades
        path.left(90)  # Gira 90 grados a la izquierda

    path.end_fill()  # Finaliza el relleno del cuadrado

def offset(point):  # Convierte las coordenadas del punto en un índice dentro de la lista de tiles
    x = (floor(point.x, 20) + 200) / 20  # Redondea las coordenadas al múltiplo más cercano de 20 y las convierte en índice
    y = (180 - floor(point.y, 20)) / 20  # Hace lo mismo para el eje y
    index = int(x + y * 20)  # Calcula el índice de la lista de tiles
    return index

def valid(point):  # Verifica si un punto es válido dentro del mapa
    index = offset(point)  # Obtiene el índice correspondiente al punto

    if tiles[index] == 0:  # Si el tile en esa posición es 0 (vacío), no es válido
        return False

    index = offset(point + 19)  # Verifica también si el siguiente punto (más a la derecha o abajo) es válido

    if tiles[index] == 0:  # Si el tile en esa posición es 0 (vacío), no es válido
        return False

    return point.x % 20 == 0 or point.y % 20 == 0  # Asegura que la posición esté alineada con la cuadrícula

def world():  # Dibuja el mundo (el mapa de juego)
    bgcolor('black')  # Establece el fondo negro
    path.color('blue')  # Establece el color de la ruta como azul

    for index in range(len(tiles)):  # Itera a través de todos los tiles
        tile = tiles[index]  # Obtiene el valor del tile en la posición actual

        if tile > 0:  # Si el tile no es vacío
            x = (index % 20) * 20 - 200  # Calcula la posición x del tile
            y = 180 - (index // 20) * 20  # Calcula la posición y del tile
            square(x, y)  # Dibuja el cuadrado en la posición

            if tile == 1:  # Si el tile es un camino (1)
                path.up()
                path.goto(x + 10, y + 10)  # Mueve el lápiz al centro del tile
                path.dot(2, 'white')  # Dibuja un punto blanco (la comida)

def move():  # Función que mueve a Pacman y a los fantasmas
    writer.undo()  # Borra el puntaje anterior
    writer.write(state['score'])  # Escribe el puntaje actual

    clear()  # Limpia la pantalla para redibujar

    if valid(pacman + aim):  # Si el siguiente movimiento de Pacman es válido
        pacman.move(aim)  # Mueve a Pacman

    index = offset(pacman)  # Obtiene el índice del tile donde se encuentra Pacman

    if tiles[index] == 1:  # Si el tile es una comida (1)
        tiles[index] = 2  # Marca el tile como comido (2)
        state['score'] += 1  # Aumenta el puntaje
        x = (index % 20) * 20 - 200  # Calcula la posición del tile
        y = 180 - (index // 20) * 20
        square(x, y)  # Dibuja el tile con la comida comido

    up()  # Levanta el lápiz para mover a Pacman
    goto(pacman.x + 10, pacman.y + 10)  # Mueve el lápiz a la posición de Pacman
    dot(20, 'yellow')  # Dibuja a Pacman como un círculo amarillo

    for point, course in ghosts:  # Mueve los fantasmas
        if valid(point + course):  # Si el movimiento del fantasma es válido
            point.move(course)  # Mueve al fantasma
        else:  # Si no es válido, elige un nuevo movimiento aleatorio
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)  # Selecciona un movimiento aleatorio
            course.x = plan.x
            course.y = plan.y

        up()  # Levanta el lápiz para mover el fantasma
        goto(point.x + 10, point.y + 10)  # Mueve el lápiz a la posición del fantasma
        dot(20, 'red')  # Dibuja al fantasma como un círculo rojo

    update()  # Actualiza la pantalla

    for point, course in ghosts:  # Verifica si Pacman colisiona con algún fantasma
        if abs(pacman - point) < 20:  # Si la distancia entre Pacman y un fantasma es menor a 20
            return  # Termina el juego si hay colisión

    ontimer(move, 100)  # Llama a la función move nuevamente después de 100ms

def change(x, y):  # Cambia la dirección de Pacman si es válida
    if valid(pacman + vector(x, y)):  # Si la dirección es válida
        aim.x = x  # Cambia la dirección en x
        aim.y = y  # Cambia la dirección en y

setup(420, 420, 370, 0)  # Establece el tamaño y la posición de la ventana de juego
hideturtle()  # Oculta el cursor de la tortuga
tracer(False)  # Desactiva la actualización automática de la pantalla
writer.goto(160, 160)  # Establece la posición del escritor (donde se muestra el puntaje)
writer.color('white')  # Establece el color de texto como blanco
writer.write(state['score'])  # Escribe el puntaje inicial
listen()  # Escucha las teclas presionadas
onkey(lambda: change(5, 0), 'Right')  # Si se presiona la tecla 'Right', mueve a la derecha
onkey(lambda: change(-5, 0), 'Left')  # Si se presiona la tecla 'Left', mueve a la izquierda
onkey(lambda: change(0, 5), 'Up')  # Si se presiona la tecla 'Up', mueve hacia arriba
onkey(lambda: change(0, -5), 'Down')  # Si se presiona la tecla 'Down', mueve hacia abajo
world()  # Dibuja el mundo (el mapa)
move()  # Inicia el movimiento de Pacman y los fantasmas
done()  # Finaliza el juego

