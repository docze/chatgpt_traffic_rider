import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        color = random.choice(["green", "yellow", "red"])
        self.image = pygame.image.load(
            f"assets/{color}-car.png").convert_alpha()
        if (speed < 0):
            self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed
        # check for collision with other enemies
        for enemy in args[0]:
            if self != enemy:
                if self.rect.colliderect(enemy.rect.inflate(20, 25)):
                    if self.speed > enemy.speed:
                        self.speed = enemy.speed
                    elif self.speed < enemy.speed:
                        enemy.speed = self.speed
                    break
        if self.rect.top > 800 or self.rect.top < -32:
            self.kill()
