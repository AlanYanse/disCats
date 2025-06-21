
import pygame
import sys

from config import *
from niveles import *
from funciones import *

class Game:

    def __init__(self):

        self.program_runnig = True

        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        self.num_tile = get_diccionario_tiles(self)

        self.scroll_x = 0




    def update(self):
        
        tecla_presionada = pygame.key.get_pressed()
        
        if tecla_presionada[pygame.K_RIGHT]:
            self.scroll_x += 5
        elif tecla_presionada[pygame.K_LEFT]:
            self.scroll_x -= 5

        pygame.display.flip()
        self.reloj.tick(60) # Para que se refresque a 60 FPS


    def draw(self):
        
        self.screen.fill(BLANCO)
        draw_tilemap_buena(self)



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



    def obtener_grafico(self, nombre_archivo):
        #img = pygame.image.load(f"assets/{nombre_archivo}").convert()
        img = pygame.image.load(f"assets/{nombre_archivo}").convert()
        escala_x = 64
        escala_y = 64
        image = pygame.transform.scale(img, (escala_x,escala_y)) # Para escalar los tiles
        image.set_colorkey(BLANCO)
        rect = image.get_rect() # Hay que obtener el rectangulo para poder interactuar con los tiles
        return (image, rect)
