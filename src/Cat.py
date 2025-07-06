
import pygame


class Cat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.direccion = 'abajo'
        self.indice_animacion = 0
        self.spritesheet = spritesheet = pygame.image.load("assets/sprite_sheet_bk.png").convert_alpha()  # Usa tu imagen subida


        # Animaciones por dirección (fila en el sprite sheet)
        self.animaciones = {
            'abajo': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],  # elige los frames de la fila 0 columnas 0,1,2,3
            'izquierda': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],  # elige los frames de la fila 0 columnas 0,1,2,3
            'derecha': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]],  # elige los frames de la fila 0 columnas 0,1,2,3
            'arriba': [self.obtener_frame(0, i) for i in [0, 1, 2, 3]]  # elige los frames de la fila 0 columnas 0,1,2,3
}
        self.image = self.animaciones[self.direccion][self.indice_animacion]
        self.rect = self.image.get_rect()
        # Posicionar rect
        self.rect.topleft = (x, y)
        self.velocidad = 3
        self.contador_animacion = 0

    def update(self, teclas):
        dx = dy = 0
        nueva_direccion = self.direccion

        if teclas[pygame.K_LEFT] and self.game.scroll_x > 0:
            dx = -self.velocidad
            self.game.scroll_x -= 2
            nueva_direccion = 'izquierda'
        elif teclas[pygame.K_RIGHT] and self.game.scroll_x < 420:
            dx = self.velocidad
            self.game.scroll_x += 2
            nueva_direccion = 'derecha'
        elif teclas[pygame.K_UP]:
            dy = -self.velocidad
            nueva_direccion = 'arriba'
        elif teclas[pygame.K_DOWN]:
            dy = self.velocidad
            nueva_direccion = 'abajo'

        # Si no hay movimiento, resetear animación a primer frame
        if dx == 0 and dy == 0:
            self.indice_animacion = 0
            self.image = self.animaciones[self.direccion][self.indice_animacion]
            return

        # Actualiza la dirección si hay movimiento
        if nueva_direccion != self.direccion:
            self.direccion = nueva_direccion
            self.indice_animacion = 0  # Reinicia animación al cambiar dirección

        # Animación
        self.contador_animacion += 1
        if self.contador_animacion >= 5:  # Velocidad de animación
            self.contador_animacion = 0
            self.indice_animacion = (self.indice_animacion + 1) % len(self.animaciones[self.direccion])
            self.image = self.animaciones[self.direccion][self.indice_animacion]

        # Mover el sprite
        self.rect.x += dx
        self.rect.y += dy


    def obtener_frame(self, fila, columna, ancho=64, alto=64):
        """Obtiene un frame del sprite sheet dada una fila y columna"""
        x = columna * ancho
        y = fila * alto
        imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        imagen.blit(self.spritesheet, (0, 0), (x, y, ancho, alto))
        return imagen
