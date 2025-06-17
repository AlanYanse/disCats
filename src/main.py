
import pygame
import sys


from Game import *
from Cat import *  # si guardás la clase en un archivo llamado cat.py


if __name__ == '__main__':

    game = Game()
    game.bucle_principal()


"""
pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("disCats")

# Crear una instancia de Cat
gato = Cat("assets/sprite_sheet_bk.png", filas=2, columnas=4, tamanio=(96, 96), pos=(50, 50))

clock = pygame.time.Clock()

while True:

    pantalla.fill((255, 255, 255)) # Pinta la pantalla de blanco

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    gato.actualizar()
    gato.dibujar(pantalla)

    pygame.display.flip()
    clock.tick(60)
"""
