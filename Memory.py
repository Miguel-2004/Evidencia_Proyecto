from random import *
from turtle import *
from freegames import path

car = path('car.gif')
# Cambio del número de tarjetas
tiles = list(range(50)) * 2
state = {'mark': None}
# Adaptación al número declarado arriba
hide = [True] * 100
# Declaración de variable "pares" para acumular pares descubiertos
pares = 0

def square(x, y):
    "Draw white square with black outline at (x, y)."
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        # Adaptación de las unidades para hacer el tablero del mismo tamaño
        forward(45)
        left(90)
    end_fill()

# Cambio para adaptar coordenadas a nuevo número de tarjetas (en 'index' y 'xy')
def index(x, y):
    "Convert (x, y) coordinates to tiles index."
    return int((x + 250) // 45 + ((y + 250) // 45) * 10)

def xy(count):
    "Convert tiles count to (x, y) coordinates."
    return (count % 10) * 45 - 250, (count // 10) * 45 - 250

def tap(x, y):
    "Update mark and hidden tiles based on tap."
    # Uso de variable global para acumulación general
    global pares
    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        # Aumento a variable cuando un par es encontrado
        pares += 1
        state['mark'] = None

def draw():
    "Draw image and tiles."
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    # Adaptación a las 100 tarjetas
    for count in range(100):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    # Comprobar que todos los pares han sido descubiertos
    if all(not i for i in hide):
        # Desplegar mensaje de juego terminado
        up()
        goto(-200, 0)
        color('red')
        write("Juego terminado :D", font = ('Arial', 30, 'normal'))
        return

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    # Despliegue de pares encontrados
    up()
    goto(-200, 200)
    color('green')
    write(f'Pares encontrados: {pares}', font = ('Arial', 30, 'normal'))
    update()
    ontimer(draw, 100)

shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
Logo