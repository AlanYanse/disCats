
import pygame
import sys

from config import *

class Game:

    def __init__(self):

        self.program_runnig = True

        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()


    def update(self):
        pygame.display.flip()
        self.reloj.tick(60) # Para que se refresque a 60 FPS


    def draw(self):
        pass


    def check_event(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.program_runnig = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.program_runnig = False
                    pygame.quit()
                    sys.exit()




    def bucle_principal(self):
        self.screen.fill(BLANCO) # Pinta la pantalla de blanco
        while self.program_runnig:
            self.check_event()
            self.update()
            self.draw()
