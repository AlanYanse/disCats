
import pygame

class Cat:

    def __init__(self, sprite_path, filas, columnas, tamanio=(64,64), pos=(100,100), tiempo_frame=100):

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha() # define la hoja de sprites del personaje
        self.filas = filas
        self.columnas = columnas
        self.tamanio_frame = tamanio
        self.pos = pos
        self.tiempo_frame = tiempo_frame
        self.vidas = 7
        self.estado = ["invisible", "pequenio", "super_heroe"]


        self.frames = self.cargar_frames()
        self.indice = 0
        self.ultimo_cambio = pygame.time.get_ticks()
        
    
    def cargar_frames(self):

        ancho_sprite = self.sprite_sheet.get_width() // self.columnas
        alto_sprite = self.sprite_sheet.get_height() // self.filas

        frames = []
        for fila in range(self.filas):
            for col in range(self.columnas):
                frame = self.sprite_sheet.subsurface(
                    (col * ancho_sprite, fila * alto_sprite, ancho_sprite, alto_sprite)
                )
                frame_escalado = pygame.transform.scale(frame, self.tamanio_frame)
                frames.append(frame_escalado)
        return frames
    

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_cambio > self.tiempo_frame:
            self.indice = (self.indice + 1) % len(self.frames)
            self.ultimo_cambio = ahora

    
    def dibujar(self, pantalla):
        pantalla.blit(self.frames[self.indice], self.pos)


    