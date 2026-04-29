import pygame
import random

# --- CONFIGURACIÓN ---
ANCHO_CELDA = 40

# --- CONFIGURACIÓN DEL MAPA MEJORADO (19x15) ---
# 1: Pared, 0: Punto, 2: Inicio Jugador, 4: Enemigo
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Colores
NEGRO = (0, 0, 0)
AZUL = (50, 150, 255)    # Jugador
ROJO = (255, 50, 50)     # Enemigo
GRIS = (100, 100, 100)   # Paredes
AMARILLO = (255, 255, 0) # Puntos
BLANCO = (255, 255, 255)

class Enemigo:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def mover(self, tablero):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)
        for dr, dc in direcciones:
            nr, nc = self.r + dr, self.c + dc
            if 0 <= nr < len(tablero) and 0 <= nc < len(tablero[0]):
                if tablero[nr][nc] != 1:
                    self.r, self.c = nr, nc
                    break

def main():
    pygame.init()
    columnas = len(MAPA[0])
    filas = len(MAPA)
    # Ajustamos la pantalla dinámicamente según el tamaño del mapa
    pantalla = pygame.display.set_mode((columnas * ANCHO_CELDA, filas * ANCHO_CELDA + 50))
    pygame.display.set_caption("Pac-Man Extendido")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 22, bold=True)

    # Inicializar datos
    tablero = [fila[:] for fila in MAPA]
    pos_p = [1, 1]
    enemigos = []
    puntos_totales = 0
    vidas = 3
    
    for r in range(filas):
        for c in range(columnas):
            if tablero[r][c] == 4: 
                enemigos.append(Enemigo(r, c))
                tablero[r][c] = 3 
            if tablero[r][c] == 0: 
                puntos_totales += 1

    puntuacion = 0
    corriendo = True
    ganado = False

    while corriendo:
        pantalla.fill(NEGRO)
        
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if evento.type == pygame.KEYDOWN and vidas > 0 and not ganado:
                nr, nc = pos_p[0], pos_p[1]
                if evento.key == pygame.K_w: nr -= 1
                elif evento.key == pygame.K_s: nr += 1
                elif evento.key == pygame.K_a: nc -= 1
                elif evento.key == pygame.K_d: nc += 1
                
                # Movimiento jugador
                if 0 <= nr < filas and 0 <= nc < columnas:
                    if tablero[nr][nc] != 1:
                        if tablero[nr][nc] == 0:
                            puntuacion += 1
                            tablero[nr][nc] = 3 
                        pos_p = [nr, nc]
                        
                        # Movimiento enemigos
                        for e in enemigos:
                            e.mover(tablero)

        # 2. Lógica de Colisión
        for e in enemigos:
            if e.r == pos_p[0] and e.c == pos_p[1]:
                vidas -= 1
                pos_p = [1, 1] # Resetear posición del jugador
                if vidas <= 0:
                    vidas = 0 

        # 3. Dibujado
        for r in range(filas):
            for c in range(columnas):
                rect = (c * ANCHO_CELDA, r * ANCHO_CELDA, ANCHO_CELDA, ANCHO_CELDA)
                if tablero[r][c] == 1:
                    pygame.draw.rect(pantalla, GRIS, rect)
                elif tablero[r][c] == 0:
                    pygame.draw.circle(pantalla, AMARILLO, (c * ANCHO_CELDA + 20, r * ANCHO_CELDA + 20), 5)
        
        # Dibujar Jugador y Enemigos
        if vidas > 0:
            pygame.draw.rect(pantalla, AZUL, (pos_p[1] * ANCHO_CELDA + 5, pos_p[0] * ANCHO_CELDA + 5, 30, 30))
            for e in enemigos:
                pygame.draw.rect(pantalla, ROJO, (e.c * ANCHO_CELDA + 5, e.r * ANCHO_CELDA + 5, 30, 30))

        # Interfaz de Usuario
        txt_puntos = fuente.render(f"Puntos: {puntuacion}/{puntos_totales}", True, BLANCO)
        txt_vidas = fuente.render(f"Vidas: {'❤️' * vidas}", True, ROJO)
        pantalla.blit(txt_puntos, (10, filas * ANCHO_CELDA + 15))
        pantalla.blit(txt_vidas, (columnas * ANCHO_CELDA - 150, filas * ANCHO_CELDA + 15))

        # Mensajes de Fin de Juego
        if vidas == 0:
            msg = fuente.render("GAME OVER - Pulsa ESC para salir", True, ROJO)
            pantalla.blit(msg, (columnas * ANCHO_CELDA // 2 - 140, filas * ANCHO_CELDA // 2))
        
        if puntuacion == puntos_totales:
            ganado = True
            msg