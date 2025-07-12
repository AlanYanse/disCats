import pygame

class Cat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.direccion = 'abajo'
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
        dx = dy = 0
        nueva_direccion = self.direccion

        # Solo permitir movimiento horizontal si está en el suelo
        if self.en_suelo:
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

        # Salto (solo si está en el suelo)
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.velocidad_y = self.velocidad_salto
            self.en_suelo = False
            nueva_direccion = 'salto'
            self.indice_animacion = 0  # Reiniciar animación de salto

        # Aplicar gravedad
        self.velocidad_y += self.gravedad
        dy += self.velocidad_y

        # Verificar colisión con el suelo (aquí asumimos que el suelo está en y=400)
        if self.rect.bottom + dy > 400:  # Ajusta este valor según tu juego
            dy = 400 - self.rect.bottom
            self.velocidad_y = 0
            self.en_suelo = True
            if self.direccion == 'salto':
                nueva_direccion = 'abajo'  # Volver a animación normal al tocar el suelo
        else:
            self.en_suelo = False


        # Si no hay movimiento, resetear animación a primer frame
        if dx == 0 and dy == 0:
            self.indice_animacion = 0
            frame = self.animaciones[self.direccion][self.indice_animacion]
            if self.direccion == 'izquierda':
                frame = pygame.transform.flip(frame, True, False)
            self.image = frame
            return

        # Actualiza la dirección si hay cambio
        if nueva_direccion != self.direccion:
            self.direccion = nueva_direccion
            self.indice_animacion = 0

        # Animación
        self.contador_animacion += 1
        if self.contador_animacion >= 5:  # Velocidad de animación
            self.contador_animacion = 0
            if not self.en_suelo and self.direccion != 'salto':
                self.direccion = 'salto'  # Cambiar a animación de salto si está en el aire
                self.indice_animacion = 0

            self.indice_animacion = (self.indice_animacion + 1) % len(self.animaciones[self.direccion])
            frame = self.animaciones[self.direccion][self.indice_animacion]

            # Volteo horizontal para movimiento a la izquierda
            if self.direccion in ['izquierda', 'salto'] and dx < 0:
                frame = pygame.transform.flip(frame, True, False)
            elif self.direccion == 'salto' and self.direccion_prev in ['derecha', 'abajo']:
                frame = pygame.transform.flip(frame, False, False)

            self.image = frame

        # Guardar dirección previa para salto
        if self.en_suelo and self.direccion != 'salto':
            self.direccion_prev = self.direccion

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
