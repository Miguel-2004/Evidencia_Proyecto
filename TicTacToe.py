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

def check_winner():
    """Check if there is a winner."""
    board = state['board']

    # Verificar filas
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]  # Retorna el jugador que ganó (0 o 1)

    # Verificar columnas
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]  # Retorna el jugador que ganó (0 o 1)

    # Verificar diagonales
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]  # Retorna el jugador que ganó (0 o 1)
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]  # Retorna el jugador que ganó (0 o 1)

    # Verificar empate
    if all(cell is not None for row in board for cell in row):
        return "draw"  # Retorna "draw" si hay un empate

    return None  # No hay ganador ni empate

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

    # Verificar si hay un ganador o empate
    winner = check_winner()
    if winner is not None:
        goto(-100, 0)  # Mover el cursor para escribir el mensaje
        if winner == "draw":
            write("Empate!", font=("Arial", 36, "normal"))  # Mostrar mensaje de empate
        else:
            write(f"Jugador {winner + 1} gana!", font=("Arial", 36, "normal"))  # Mostrar mensaje de ganador
        return  # Terminar el juego

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