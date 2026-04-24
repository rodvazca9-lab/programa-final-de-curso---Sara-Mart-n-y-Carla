import pygame
import random

# --- CONFIGURACIÓN ---
ANCHO_CELDA = 40
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 4, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
        self.timer_movimiento = 0 # Para que no se muevan demasiado rápido

    def mover(self, tablero):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcciones)
        for dr, dc in direcciones:
            nr, nc = self.r + dr, self.c + dc
            if tablero[nr][nc] != 1 and tablero[nr][nc] != 4:
                self.r, self.c = nr, nc
                break

def main():
    pygame.init()
    columnas = len(MAPA[0])
    filas = len(MAPA)
    pantalla = pygame.display.set_mode((columnas * ANCHO_CELDA, filas * ANCHO_CELDA + 50))
    pygame.display.set_caption("Pac-Man Clone Pygame")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 24)

    # Inicializar datos
    tablero = [fila[:] for fila in MAPA]
    pos_p = [1, 1]
    enemigos = []
    puntos_totales = 0
    
    for r in range(filas):
        for c in range(columnas):
            if tablero[r][c] == 4: enemigos.append(Enemigo(r, c))
            if tablero[r][c] == 0: puntos_totales += 1

    puntuacion = 0
    corriendo = True

    while corriendo:
        pantalla.fill(NEGRO)
        
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if evento.type == pygame.KEYDOWN:
                nr, nc = pos_p[0], pos_p[1]
                if evento.key == pygame.K_w: nr -= 1
                if evento.key == pygame.K_s: nr += 1
                if evento.key == pygame.K_a: nc -= 1
                if evento.key == pygame.K_d: nc += 1
                
                # Lógica de movimiento jugador
                if tablero[nr][nc] != 1:
                    if tablero[nr][nc] == 0:
                        puntuacion += 1
                        tablero[nr][nc] = 3 # Limpiar punto
                    pos_p = [nr, nc]
                    
                    # Los enemigos se mueven cada vez que el jugador se mueve
                    for e in enemigos:
                        e.mover(tablero)

        # 2. Lógica de Colisión (Muerte)
        for e in enemigos:
            if e.r == pos_p[0] and e.c == pos_p[1]:
                print("¡GAME OVER!")
                corriendo = False

        # 3. Dibujado
        for r in range(filas):
            for c in range(columnas):
                rect = (c * ANCHO_CELDA, r * ANCHO_CELDA, ANCHO_CELDA, ANCHO_CELDA)
                if tablero[r][c] == 1:
                    pygame.draw.rect(pantalla, GRIS, rect)
                elif tablero[r][c] == 0:
                    pygame.draw.circle(pantalla, AMARILLO, (c * ANCHO_CELDA + 20, r * ANCHO_CELDA + 20), 5)
        
        # Dibujar Jugador
        pygame.draw.rect(pantalla, AZUL, (pos_p[1] * ANCHO_CELDA + 5, pos_p[0] * ANCHO_CELDA + 5, 30, 30))
        
        # Dibujar Enemigos
        for e in enemigos:
            pygame.draw.rect(pantalla, ROJO, (e.c * ANCHO_CELDA + 5, e.r * ANCHO_CELDA + 5, 30, 30))

        # Interfaz
        texto = fuente.render(f"Puntos: {puntuacion} / {puntos_totales}", True, BLANCO)
        pantalla.blit(texto, (10, filas * ANCHO_CELDA + 10))

        if puntuacion == puntos_totales:
            win_text = fuente.render("¡GANASTE!", True, AMARILLO)
            pantalla.blit(win_text, (columnas * ANCHO_CELDA // 2 - 40, filas * ANCHO_CELDA // 2))

        pygame.display.flip()


        
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()