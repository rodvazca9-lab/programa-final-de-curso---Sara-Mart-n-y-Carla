import turtle
from freegames import floor, vector

# Configuración inicial
screen = turtle.Screen()
screen.setup(420, 420)
state = {'score': 0}
path = turtle.Turtle(visible=False)
writer = turtle.Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)

# El mapa: 1 es pared, 0 es camino con punto
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
    0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0,
    0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    """Dibuja un cuadrado en las coordenadas x, y."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    """Calcula el índice del tile basado en la posición."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """Retorna True si el movimiento es válido (no hay pared)."""
    index = offset(point)
    if tiles[index] == 1:
        return False
    index = offset(point + 19)
    if tiles[index] == 1:
        return False
    return point.x > -200 and point.x < 190 and point.y > -200 and point.y < 190

def world():
    """Dibuja el mundo (paredes y puntos)."""
    path.color('blue')
    for index, tile in enumerate(tiles):
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
        elif tile == 0:
            x = (index % 20) * 20 - 200 + 10
            y = 180 - (index // 20) * 20 + 10
            path.up()
            path.goto(x, y)
            path.dot(2, 'white')

def move():
    """Mueve a Pac-Man y actualiza el juego."""
    writer.undo()
    writer.write(state['score'])
    
    # Intentar mover
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Si hay un punto (0), comerlo
    if tiles[index] == 0:
        tiles[index] = 2 # 2 significa vacío
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    turtle.clear()
    turtle.up()
    turtle.goto(pacman.x + 10, pacman.y + 10)
    turtle.dot(20, 'yellow')
    
    turtle.update()
    turtle.ontimer(move, 100)

def change(x, y):
    """Cambia la dirección de Pac-Man."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# Configuración de controles
screen.bgcolor('black')
turtle.tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
screen.listen()
screen.onkey(lambda: change(5, 0), 'Right')
screen.onkey(lambda: change(-5, 0), 'Left')
screen.onkey(lambda: change(0, 5), 'Up')
screen.onkey(lambda: change(0, -5), 'Down')

world()
move()
turtle.done()