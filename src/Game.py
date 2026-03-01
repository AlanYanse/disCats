
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
        pygame.mixer.init() # Para la música

        self.musica_menu = f"assets/Music/{MUSICA_MENU}"
        self.volumen_menu = VOLUMEN_MENU

        self.musica_nivel_1 = f"assets/Music/{MUSICA_NIVEL_1}"
        self.volumen_nivel_1 = VOLUMEN_NIVEL_1

        self.checkpoint_actual = 0

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

        # --- IMÁGENES MENÚ ---
        self.img_titulo = pygame.image.load("assets/Menu/label-discats.png").convert_alpha()
        self.img_play = pygame.image.load("assets/Menu/label-play.png").convert_alpha()
        self.img_salir = pygame.image.load("assets/Menu/label-salir.png").convert_alpha()

        # Rectángulos (para colisión)
        self.rect_titulo = self.img_titulo.get_rect(center=(ANCHO//2, 120))
        self.rect_play = self.img_play.get_rect(center=(ANCHO//2, 300))
        self.rect_salir = self.img_salir.get_rect(center=(ANCHO//2, 420))

        # Índice de selección
        self.opcion_seleccionada = 0  # 0 = Play, 1 = Salir

        pygame.mixer.music.load(self.musica_menu)
        pygame.mixer.music.set_volume(self.volumen_menu)
        pygame.mixer.music.play(-1)  # loop infinito

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

        # NO actualizar nada si estamos en el menú
        if not self.estado_juego["en_juego"]:
            return

        teclas = pygame.key.get_pressed()
        self.listas_sprites["all_sprites"].update(teclas)

        if hasattr(self, "gato"):

            # --- COLISIÓN CON ARÁNDANOS ---
            arandanos_colision = pygame.sprite.spritecollide(
                self.gato,
                self.listas_sprites["arandanos"],
                True
            )

            if arandanos_colision:
                self.puntos += 10 * len(arandanos_colision)
                print("Puntos actuales:", self.puntos)

            # --- COLISIÓN CON CEREZAS ---
            cerezas_colision = pygame.sprite.spritecollide(
                self.gato,
                self.listas_sprites["cerezas"],
                True
            )

            if cerezas_colision and self.vidas < VIDAS_MAXIMAS:
                self.vidas += 1
                print("VIDAS:", self.vidas)

            # --- COLISIÓN CON CARBONES ---
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
            self.scroll_x = self.gato.rect.centerx - ANCHO // 2
            max_scroll = COLUMNAS * 64 - ANCHO

            if self.scroll_x < 0:
                self.scroll_x = 0
            if self.scroll_x > max_scroll:
                self.scroll_x = max_scroll

            # --- ACTUALIZAR CHECKPOINT (optimizado) ---
            for i in range(len(CHECKPOINTS)):
                if self.gato.rect.x >= CHECKPOINTS[i][0]:
                    self.checkpoint_actual = i
                else:
                    break

            # --- MUERTE POR CAÍDA ---
            if self.gato.rect.bottom > LIMITE_CAIDA:
                self.respawnear_gato()

        self.reloj.tick(60)


    def draw(self):

        # ----- MENÚ -----
        if self.estado_juego["menu_presentacion"]:
            self.draw_menu_presentacion()
            return

        # ----- JUEGO -----
        self.screen.fill(BLANCO)

        for sprite in self.listas_sprites["all_sprites"]:
            self.screen.blit(
                sprite.image,
                (sprite.rect.x - self.scroll_x, sprite.rect.y)
            )


    def iniciar_juego(self):

        self.resetear_estados_juego()
        self.estado_juego["en_juego"] = True

        pygame.mixer.music.stop()

        pygame.mixer.music.load(self.musica_nivel_1)
        pygame.mixer.music.set_volume(self.volumen_nivel_1)
        pygame.mixer.music.play(-1)

        if self.vidas <= 0:
            self.vidas = 7
            self.puntos = 0
            self.nivel = 1

        self.new_game()



    def check_event(self):

        for event in pygame.event.get():

            # ---- SALIR GLOBAL ----
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # ======================================================
            # ===================== MENÚ ============================
            # ======================================================

            if self.estado_juego["menu_presentacion"]:

                # -------- TECLADO --------
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % 2

                    if event.key == pygame.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % 2

                    if event.key == pygame.K_RETURN:
                        if self.opcion_seleccionada == 0:
                            self.iniciar_juego()
                        else:
                            pygame.quit()
                            sys.exit()

                # -------- MOUSE --------
                mouse_pos = pygame.mouse.get_pos()

                if self.rect_play.collidepoint(mouse_pos):
                    self.opcion_seleccionada = 0

                if self.rect_salir.collidepoint(mouse_pos):
                    self.opcion_seleccionada = 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.opcion_seleccionada == 0:
                            self.iniciar_juego()
                        else:
                            pygame.quit()
                            sys.exit()

            # ======================================================
            # ===================== JUEGO ===========================
            # ======================================================

            elif self.estado_juego["en_juego"]:

                if event.type == self.spawn_carbon_event:
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


    def draw_menu_presentacion(self):

        self.screen.fill((240, 240, 240))

        # Título
        self.screen.blit(self.img_titulo, self.rect_titulo)

        # Resaltar opción seleccionada
        if self.opcion_seleccionada == 0:
            pygame.draw.rect(self.screen, (0,0,0), self.rect_play.inflate(20,10), 3)
        else:
            pygame.draw.rect(self.screen, (0,0,0), self.rect_salir.inflate(20,10), 3)

        # Botones
        self.screen.blit(self.img_play, self.rect_play)
        self.screen.blit(self.img_salir, self.rect_salir)



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

    
    def respawnear_gato(self):

        self.vidas -= 1

        if self.vidas <= 0:
            self.ir_gameover()
            return

        x, y = CHECKPOINTS[self.checkpoint_actual]

        self.gato.rect.topleft = (x, y)
        self.gato.velocidad_y = 0
        self.gato.en_suelo = False

        self.scroll_x = x - ANCHO // 2
        if self.scroll_x < 0:
            self.scroll_x = 0


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
