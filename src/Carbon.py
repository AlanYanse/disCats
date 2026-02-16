import pygame

from config import *

class Carbon(pygame.sprite.Sprite):

    def __init__(self, game, x, y, image):
        super().__init__()
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.velocidad = VELOCIDAD_CARBON

    def update(self, teclas=None):
        self.rect.x -= self.velocidad

        if self.rect.right < 0:
            self.kill()