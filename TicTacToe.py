from turtle import *
from freegames import line

def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)

def drawx(x, y):
    """Draw X player."""
    color("blue")  # Cambia el color a azul
    width(5)       # Cambia el grosor de la línea
    line(x, y, x + 133, y + 133)
    line(x, y + 133, x + 133, y)

def drawo(x, y):
    """Draw O player."""
    color("red")   # Cambia el color a rojo
    width(5)       # Cambia el grosor de la línea
    up()
    goto(x + 67, y + 5)
    down()
    circle(62)

def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200

# Estado inicial del juego
state = {'player': 0, 'board': [[None, None, None], [None, None, None], [None, None, None]]}
players = [drawx, drawo]

def tap(x, y):
    """Draw X or O in tapped square."""
    x = floor(x)
    y = floor(y)
    row = int((y + 200) // 133)  # Convertir coordenadas a fila
    col = int((x + 200) // 133)  # Convertir coordenadas a columna

    # Validar si la casilla ya está ocupada
    if state['board'][row][col] is not None:
        return  # Casilla ocupada, no hacer nada

    # Obtener el jugador actual (0 para X, 1 para O)
    player = state['player']
    draw = players[player]  # Seleccionar la función de dibujo (drawx o drawo)

    # Dibujar la marca (X o O) en la casilla
    draw(x, y)

    # Actualizar el estado del tablero
    state['board'][row][col] = player

    # Cambiar al siguiente jugador
    state['player'] = not player

    # Actualizar la pantalla
    update()

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)
done()