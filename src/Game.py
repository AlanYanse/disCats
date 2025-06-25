
import pygame
import sys

from config import *
from niveles import *
from funciones import *

class Game:

    def __init__(self):

        pygame.init()

        self.program_runnig = True

        self.puntos = 0
        self.vidas = 3
        self.nivel = 1

        self.estado_juego = {

            "menu_presentacion": True,
            "en_juego": False,
            "game_over": False,
            "nivel_superado": False

        }

        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        # Iniciar las listas de sprites
        self.listas_sprites = {
            "all_sprites": pygame.sprite.Group(),
            "catsito": pygame.sprite.Group(),
            "escenario": pygame.sprite.Group(),
            "textos": pygame.sprite.Group()
        }

        self.fuente = pygame.font.SysFont("verdana", 48)
        self.txt_enter = self.fuente.render("Pulsar enter para continuar", True, (0,0,0))

        self.num_tile = get_diccionario_tiles(self)

        self.scroll_x = 0




    def update(self):

        """ tecla_presionada = pygame.key.get_pressed()
        limite_provisorio = 380

        if tecla_presionada[pygame.K_RIGHT] and self.scroll_x < limite_provisorio:
            self.scroll_x += 5
            print(self.scroll_x)
        elif tecla_presionada[pygame.K_LEFT] and self.scroll_x > 0:
            self.scroll_x -= 5 """

        pygame.display.flip()
        self.reloj.tick(60) # Para que se refresque a 60 FPS


    def draw(self):

        self.screen.fill(BLANCO)
        draw_tilemap_buena(self)

        if self.estado_juego["menu_presentacion"]:
            self.screen.blit(self.txt_enter, (50,100))




    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program_runnig = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.program_runnig = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN and self.estado_juego["menu_presentacion"]:
                    #pygame.mixer.music.stop() para en un futuro agregar musica
                    self.resetear_estados_juego()
                    self.estado_juego["en juego"] = True
                    if self.vidas <= 0:
                        self.vidas = 3
                        self.puntos = 0
                        self.nivel = 1
                    # Comienza el juego presionando enter
                    self.new_game()




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



    def vaciar_listas(self):
        #Vaciar todas las listas de all_sprites
        for grupo in self.listas_sprites.values():
            grupo.empty()



    def resetear_estados_juego(self):
        self.estado_juego = {clave: False for clave in self.estado_juego}




    def new_game(self):
        #Prepara un nuevo nivel o en_juego
        self.vaciar_listas()
        self.instanciar_objetos()




    def instanciar_objetos(self):
        if self.vidas <= 0:
            self.ir_gameover()
            pass
        """
        catsito = Cat()
        self.listas_sprites["all_sprites"].add(catsito)
        self.listas_sprites["catsito"].add(catsito)
        """
