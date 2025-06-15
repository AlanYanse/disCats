import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("DisCats")

# Cargar la hoja de sprites
sprite_sheet = pygame.image.load("assets/sprite_sheet_bk.png").convert_alpha()

# Parámetros del sprite sheet
CANT_FILAS = 2
CANT_COLUMNAS = 4
FRAME_ANCHO = sprite_sheet.get_width() // CANT_COLUMNAS
FRAME_ALTO = sprite_sheet.get_height() // CANT_FILAS

# Parámetros del personaje
# Hoja de sprites, posiciones, vidas, estados[], 
POS_X = 50
POS_Y = 50

# Parámetro para nuevo tamaño deseado
NUEVO_ANCHO = 96
NUEVO_ALTO = 96

# Extraer los cuadros en una lista
sprites = []
for fila in range(CANT_FILAS):
    for col in range(CANT_COLUMNAS):
        frame = sprite_sheet.subsurface((col * FRAME_ANCHO, fila * FRAME_ALTO, FRAME_ANCHO, FRAME_ALTO))
        # Escalar el frame al nuevo tamaño
        frame_escalado = pygame.transform.scale(frame, (NUEVO_ANCHO, NUEVO_ALTO))
        sprites.append(frame_escalado)
        #sprites.append(frame)

# Variables de animación
indice_frame = 0
tiempo_entre_frames = 100  # milisegundos
ultimo_cambio = pygame.time.get_ticks()

# Bucle principal
clock = pygame.time.Clock()
while True:
    pantalla.fill((255, 255, 255))  # Fondo blanco

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Animar
    ahora = pygame.time.get_ticks()
    if ahora - ultimo_cambio > tiempo_entre_frames:
        indice_frame = (indice_frame + 1) % len(sprites)
        ultimo_cambio = ahora

    # Dibujar el frame actual
    pantalla.blit(sprites[indice_frame], (POS_X, POS_Y))

    pygame.display.flip()
    clock.tick(60)
