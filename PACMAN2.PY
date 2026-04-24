import os
import time

# --- CONFIGURACIÓN DEL MAPA ---
# 1 = Pared (#), 0 = Punto (.), 2 = Jugador (P), 3 = Vacío ( ), 4 = Peligro (X)
MAPA_ORIGINAL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 4, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 4, 1, 1, 1, 1, 0, 1, 4, 1],
    [1, 0, 0, 0, 4, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def inicializar_juego():
    tablero = [fila[:] for fila in MAPA_ORIGINAL]
    pos_p = [1, 1] 
    puntos_totales = sum(fila.count(0) for fila in tablero)
    return tablero, pos_p, puntos_totales

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def dibujar_mapa(tablero, puntuacion, vidas):
    limpiar_pantalla()
    # Mostramos las vidas con un icono visual
    corazones = "❤️ " * vidas
    print(f"PUNTUACIÓN: {puntuacion}  |  VIDAS: {corazones}")
    print("-" * 30)
    for fila in tablero:
        linea = ""
        for celda in fila:
            if celda == 1: linea += "# "
            elif celda == 0: linea += ". "
            elif celda == 2: linea += "P "
            elif celda == 4: linea += "X " # Representación del peligro
            else: linea += "  "
        print(linea)
    print("-" * 30)
    print("Controles: W, A, S, D | ¡Evita las X!")

def mover_jugador(tablero, pos_actual, movimiento):
    r, c = pos_actual
    nueva_r, nueva_c = r, c

    if movimiento == 'w': nueva_r -= 1
    elif movimiento == 's': nueva_r += 1
    elif movimiento == 'a': nueva_c -= 1
    elif movimiento == 'd': nueva_c += 1
    else: return pos_actual, 0, False

    # Colisión con pared
    if tablero[nueva_r][nueva_c] == 1:
        return pos_actual, 0, False

    # Lógica de daño (si pisa un 4)
    perdio_vida = False
    if tablero[nueva_r][nueva_c] == 4:
        perdio_vida = True
        tablero[r][c] = 3 # Limpiar posición actual
        # Devolvemos al jugador al inicio [1, 1]
        tablero[1][1] = 2 
        return [1, 1], 0, perdio_vida

    # Lógica de recolección
    puntos_ganados = 1 if tablero[nueva_r][nueva_c] == 0 else 0

    # Actualizar posiciones
    tablero[r][c] = 3
    tablero[nueva_r][nueva_c] = 2
    
    return [nueva_r, nueva_c], puntos_ganados, perdio_vida

def main():
    tablero, pos_p, puntos_objetivo = inicializar_juego()
    puntuacion = 0
    vidas = 3 # Sistema de vidas inicial
    
    while vidas > 0:
        dibujar_mapa(tablero, puntuacion, vidas)
        
        if puntuacion == puntos_objetivo:
            print("\n¡FELICIDADES! Has recogido todos los puntos.")
            break

        accion = input("\nMover: ").lower()
        
        # Procesar movimiento y detectar si hubo daño
        pos_p, puntos, golpe = mover_jugador(tablero, pos_p, accion)
        
        puntuacion += puntos
        
        if golpe:
            vidas -= 1
            if vidas > 0:
                print("\n¡OUCH! Chocaste con un peligro. Menos 1 vida.")
                time.sleep(1.2)

    if vidas <= 0:
        dibujar_mapa(tablero, puntuacion, vidas)
        print("\nGAME OVER. Te has quedado sin vidas.")

if __name__ == "__main__":
    main()