import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/rider.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (350, 600)
        self.speed = 0

    def update(self):
        self.rect.x += self.speed

        if self.rect.left < 150:
            self.rect.left = 150
        elif self.rect.right > 525:
            self.rect.right = 500

    def move_left(self):
        self.speed = -5

    def move_right(self):
        self.speed = 5

    def stop(self):
        self.speed = 0
