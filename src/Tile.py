
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, scroll_x):
        screen.blit(self.image, (self.rect.x - scroll_x, self.rect.y))
