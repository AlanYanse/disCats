
import pygame
import sys

from config import *
from niveles import *
from funciones import *
from Tile import *

from Cat import *
from Arandano import *
from Carbon import *
from Cereza import *

class Game:

    def __init__(self):

        pygame.init()

        self.program_runnig = True

        self.puntos = 0
        self.vidas = VIDAS_MAXIMAS
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
            "arandanos": pygame.sprite.Group(),   # ← NUEVO
            "carbones": pygame.sprite.Group(),
            "cerezas": pygame.sprite.Group(),
            "textos": pygame.sprite.Group()
        }

        self.fuente = pygame.font.SysFont("verdana", 48)
        self.txt_enter = self.fuente.render("Pulsar enter para continuar", True, (0,0,0))

        self.spawn_carbon_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_carbon_event, FRECUENCIA_CARBON_MS)

        self.num_tile = get_diccionario_tiles(self)

        self.scroll_x = 0




    def update(self):

        teclas = pygame.key.get_pressed()
        self.listas_sprites["all_sprites"].update(teclas)

        # --- COLISIÓN CON ARÁNDANOS ---
        if hasattr(self, "gato"):
            arandanos_colision = pygame.sprite.spritecollide(
                self.gato,
                self.listas_sprites["arandanos"],
                True   # ← True los elimina automáticamente
            )

            if arandanos_colision:
                self.puntos += 10 * len(arandanos_colision)
                print("Puntos actuales:", self.puntos)  # Para debuguear
                print("Arándanos recogidos:", len(arandanos_colision))

        # --- COLISIÓN CON CEREZAS ---
        if hasattr(self, "gato"):

            cerezas_colision = pygame.sprite.spritecollide(
                self.gato,
                self.listas_sprites["cerezas"],
                True
            )

            if cerezas_colision:
                if self.vidas < VIDAS_MAXIMAS:
                    self.vidas += 1
                    print("VIDAS:", self.vidas)

        # --- COLISIÓN CON CARBONES ---
        if hasattr(self, "gato"):

            impactos = []

            for carbon in self.listas_sprites["carbones"]:
                if self.gato.rect.colliderect(carbon.hitbox):
                    impactos.append(carbon)

            for carbon in impactos:
                carbon.kill()

            if impactos:
                self.vidas -= 1
                print("VIDAS:", self.vidas)

        # --- SCROLL ---
        if hasattr(self, "gato"):

            self.scroll_x = self.gato.rect.centerx - ANCHO // 2

            #max_scroll = COLUMNAS * 64 - ANCHO
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
                    self.estado_juego["en_juego"] = True
                    if self.vidas <= 0:
                        self.vidas = 3
                        self.puntos = 0
                        self.nivel = 1
                    # Comienza el juego presionando enter
                    self.new_game()
            elif event.type == self.spawn_carbon_event:
                if self.estado_juego["en_juego"]:
                    self.spawn_carbon()




    def bucle_principal(self):
        while self.program_runnig:
            self.check_event()
            self.update()
            self.draw()
            pygame.display.flip()



    def obtener_grafico(self, nombre_archivo):
        #img = pygame.image.load(f"assets/{nombre_archivo}").convert()
        img = pygame.image.load(f"assets/{nombre_archivo}").convert_alpha()
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


    def spawn_carbon(self):

        if not hasattr(self, "gato"):
            return

        imagen_solo = self.num_tile[50][0]

        # Borde derecho de la pantalla visible
        x = self.scroll_x + ANCHO
        y = self.gato.rect.y

        carbon = Carbon(self, x, y, imagen_solo)

        self.listas_sprites["carbones"].add(carbon)
        self.listas_sprites["all_sprites"].add(carbon)

        print("Carbon creado en:", x, y)  # DEBUG


    def instanciar_objetos(self):

        if self.vidas <= 0:
            self.ir_gameover()
            return

        # Recorremos la matriz del nivel
        for y in range(FILAS):
            for x in range(COLUMNAS):

                tile_index = y * COLUMNAS + x
                tile_id = nivel_1_1[tile_index]

                # Si el tile no tiene gráfico asignado, lo ignoramos
                if tile_id not in self.num_tile or self.num_tile[tile_id] is None:
                    continue

                imagen_solo = self.num_tile[tile_id][0]
                pos_x = x * TILE_SIZE
                pos_y = y * TILE_SIZE

                # --- ARÁNDANO ---
                if tile_id == 40:
                    arandano = Arandano(pos_x, pos_y, imagen_solo)
                    self.listas_sprites["arandanos"].add(arandano)
                    self.listas_sprites["all_sprites"].add(arandano)
                # --- CEREZA ---
                elif tile_id == 60:
                    cereza = Cereza(pos_x, pos_y, imagen_solo)
                    self.listas_sprites["cerezas"].add(cereza)
                    self.listas_sprites["all_sprites"].add(cereza)

                # --- RESTO DE TILES ---
                else:
                    bloque = Tile(pos_x, pos_y, imagen_solo)

                    # Si es sólido lo añadimos al grupo de colisión
                    if tile_id in TILES_SOLIDOS:
                        self.listas_sprites["escenario"].add(bloque)

                    self.listas_sprites["all_sprites"].add(bloque)

        # Instanciamos al gato
        self.gato = Cat(self, 64, 100)
        self.listas_sprites["all_sprites"].add(self.gato)
        self.listas_sprites["catsito"].add(self.gato)

        # DEBUG opcional
        print("Arándanos creados:", len(self.listas_sprites["arandanos"]))
