import os
import time

# --- CONFIGURACIÓN DEL MAPA ---
# 1 = Pared (#), 0 = Punto (.), 2 = Jugador (P), 3 = Vacío ( )
MAPA_ORIGINAL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def inicializar_juego():
    """Prepara las variables iniciales del juego."""
    tablero = [fila[:] for fila in MAPA_ORIGINAL] # Copia profunda del mapa
    pos_p = [1, 1] # Fila, Columna inicial del jugador
    puntos_totales = sum(fila.count(0) for fila in tablero)
    return tablero, pos_p, puntos_totales

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def dibujar_mapa(tablero, puntuacion):
    """Renderiza el mapa en la consola."""
    limpiar_pantalla()
    print(f"PUNTUACIÓN: {puntuacion}")
    print("-" * 20)
    for fila in tablero:
        linea = ""
        for celda in fila:
            if celda == 1: linea += "# "
            elif celda == 0: linea += ". "
            elif celda == 2: linea += "P "
            else: linea += "  "
        print(linea)
    print("-" * 20)
    print("Controles: W (Arriba), S (Abajo), A (Izquierda), D (Derecha)")

def mover_jugador(tablero, pos_actual, movimiento):
    """Calcula y ejecuta el movimiento si es válido."""
    r, c = pos_actual
    nueva_r, nueva_c = r, c

    if movimiento == 'w': nueva_r -= 1
    elif movimiento == 's': nueva_r += 1
    elif movimiento == 'a': nueva_c -= 1
    elif movimiento == 'd': nueva_c += 1
    else: return pos_actual, 0 # Tecla no válida

    # Verificación de colisión con pared (1)
    if tablero[nueva_r][nueva_c] == 1:
        return pos_actual, 0

    # Lógica de recolección de puntos
    puntos_ganados = 0
    if tablero[nueva_r][nueva_c] == 0:
        puntos_ganados = 1

    # Actualizar posiciones en la lista de listas
    tablero[r][c] = 3 # Deja espacio vacío donde estaba
    tablero[nueva_r][nueva_c] = 2 # Nueva posición del jugador
    
    return [nueva_r, nueva_c], puntos_ganados

def main():
    """Función principal que controla el flujo del juego."""
    tablero, pos_p, puntos_objetivo = inicializar_juego()
    puntuacion = 0
    jugando = True

    while jugando:
        dibujar_mapa(tablero, puntuacion)
        
        if puntuacion == puntos_objetivo:
            print("¡FELICIDADES! Has recogido todos los puntos.")
            break

        accion = input("Mover: ").lower()
        
        # Procesar movimiento
        pos_p, puntos = mover_jugador(tablero, pos_p, accion)
        puntuacion += puntos

if __name__ == "__main__":
    main()