import pygame
from config import *

class Cat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.direccion = 'abajo'
        self.direccion_prev = None
        self.indice_animacion = 0
        self.spritesheet = pygame.image.load("assets/sprite_sheet_bk.png").convert_alpha()

        # Animaciones por dirección (fila en el sprite sheet)
        self.animaciones = {
            'abajo': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],
            'izquierda': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],
            'derecha': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],
            'arriba': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],
            'salto': [self.obtener_frame(1, i) for i in [1, 2, 3]]  # Nueva animación de salto
        }

        self.image = self.animaciones[self.direccion][self.indice_animacion]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Variables de movimiento
        self.velocidad = 3
        self.velocidad_salto = -12  # Velocidad inicial del salto (negativo porque en pygame y aumenta hacia abajo)
        self.gravedad = 0.6
        self.velocidad_y = 0
        self.en_suelo = True
        self.contador_animacion = 0
        self.contador_salto = 0

    def update(self, teclas):
        dx = 0
        dy = 0
        nueva_direccion = self.direccion

        # --- 1. ENTRADA DE TECLADO ---
        if self.en_suelo:
            if teclas[pygame.K_LEFT]:
                dx = -self.velocidad
                nueva_direccion = 'izquierda'
            elif teclas[pygame.K_RIGHT]:
                dx = self.velocidad
                nueva_direccion = 'derecha'

        # Salto
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.velocidad_y = self.velocidad_salto # -12
            self.en_suelo = False
            self.direccion_prev = self.direccion
            self.direccion = 'salto'
            self.indice_animacion = 0

        # --- 2. APLICAR GRAVEDAD ---
        self.velocidad_y += self.gravedad
        dy = self.velocidad_y

        # --- 3. COLISIÓN HORIZONTAL (EJE X) ---
        self.rect.x += dx
        # Limitar al borde izquierdo del mundo
        if self.rect.left < 0:
            self.rect.left = 0

        # Limitar al borde derecho del mundo
        ancho_mundo = COLUMNAS * 64
        if self.rect.right > ancho_mundo:
            self.rect.right = ancho_mundo
        lista_colisiones_x = pygame.sprite.spritecollide(self, self.game.listas_sprites["escenario"], False)
        for bloque in lista_colisiones_x:
            if dx > 0: # Choca moviéndose a la derecha
                self.rect.right = bloque.rect.left
            elif dx < 0: # Choca moviéndose a la izquierda
                self.rect.left = bloque.rect.right

        # --- 4. COLISIÓN VERTICAL (EJE Y) ---
        self.rect.y += dy
        self.en_suelo = False # Por defecto está en el aire
        
        lista_colisiones_y = pygame.sprite.spritecollide(self, self.game.listas_sprites["escenario"], False)
        for bloque in lista_colisiones_y:
            if self.velocidad_y > 0: # Está cayendo
                self.rect.bottom = bloque.rect.top
                self.velocidad_y = 0
                self.en_suelo = True
                if self.direccion == 'salto':
                    nueva_direccion = self.direccion_prev if self.direccion_prev else 'abajo'
            elif self.velocidad_y < 0: # Está saltando (choca con techo)
                self.rect.top = bloque.rect.bottom
                self.velocidad_y = 0

        # --- 5. LÓGICA DE ANIMACIÓN (Basada en tus fuentes) ---
        if dx == 0 and dy == 0 and self.en_suelo:
            self.indice_animacion = 0
        else:
            if nueva_direccion != self.direccion:
                self.direccion = nueva_direccion
                self.indice_animacion = 0

            self.contador_animacion += 1
            if self.contador_animacion >= 5:
                self.contador_animacion = 0
                self.indice_animacion = (self.indice_animacion + 1) % len(self.animaciones[self.direccion])

        # Seleccionar frame y aplicar volteo (flip)
        frame = self.animaciones[self.direccion][self.indice_animacion]
        if self.direccion == 'izquierda' or (self.direccion == 'salto' and self.direccion_prev == 'izquierda'):
            frame = pygame.transform.flip(frame, True, False)
        
        self.image = frame

    
    def obtener_frame(self, fila, columna, ancho=64, alto=64):
        """Obtiene un frame del sprite sheet dada una fila y columna"""
        x = columna * ancho
        y = fila * alto
        imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        imagen.blit(self.spritesheet, (0, 0), (x, y, ancho, alto))
        return imagen
