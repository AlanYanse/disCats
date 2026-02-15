
import pygame
import sys

from config import *
from niveles import *
from funciones import *
from Tile import *

from Cat import *

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

        teclas = pygame.key.get_pressed()
        self.listas_sprites["all_sprites"].update(teclas)

        # --- SCROLL ---
        if hasattr(self, "gato"):

            self.scroll_x = self.gato.rect.centerx - ANCHO // 2

            max_scroll = COLUMNAS * 64 - ANCHO

            if self.scroll_x < 0:
                self.scroll_x = 0
            if self.scroll_x > max_scroll:
                self.scroll_x = max_scroll

        self.reloj.tick(60)


    def draw(self):

        self.screen.fill(BLANCO)

        for sprite in self.listas_sprites["all_sprites"]:

            # Si es un Tile → aplicar scroll
            if isinstance(sprite, Tile):
                self.screen.blit(
                    sprite.image,
                    (sprite.rect.x - self.scroll_x, sprite.rect.y)
                )

            # Si es el gato → también aplicar scroll
            else:
                self.screen.blit(
                    sprite.image,
                    (sprite.rect.x - self.scroll_x, sprite.rect.y)
                )

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
        while self.program_runnig:
            self.check_event()
            self.update()
            self.draw()
            pygame.display.flip()



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
            return

        # Recorremos la matriz del nivel (8 filas x 18 columnas)
        for y in range(FILAS):
            for x in range(COLUMNAS):
                tile_index = y * COLUMNAS + x
                tile_id = nivel_1_1[tile_index]
                
                # Verificamos que el tile tenga un gráfico asignado
                if tile_id in self.num_tile and self.num_tile[tile_id] is not None:
                    
                    # --- SOLUCIÓN AL ERROR DE TUPLA ---
                    # Extraemos solo la imagen (índice 0) de la tupla (imagen, rect)
                    imagen_solo = self.num_tile[tile_id][0]
                    
                    # Creamos el objeto Tile con su posición real en el mundo
                    bloque = Tile(x * 64, y * 64, imagen_solo)
                    
                    # Si es el tile 10 (piso), lo añadimos al grupo de colisiones
                    if tile_id in TILES_SOLIDOS:
                        self.listas_sprites["escenario"].add(bloque)
                    
                    # Lo añadimos a all_sprites para que se dibuje
                    self.listas_sprites["all_sprites"].add(bloque)

        # Instanciamos al gato un poco más arriba para que caiga al suelo
        self.gato = Cat(self, 64, 100)
        self.listas_sprites["all_sprites"].add(self.gato)
        self.listas_sprites["catsito"].add(self.gato)
