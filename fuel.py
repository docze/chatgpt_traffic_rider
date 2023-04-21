import pygame

class Fuel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = 800
        self.rect.y = 900
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_bar_height = 200

    def update(self, dt):
            self.fuel -= dt / 1000
            if self.fuel <= 0:
                self.fuel = 0
                self.is_empty = True  # set the flag if fuel is empty
            else:
                self.is_empty = False  # reset the flag if fuel is not empty

            self.image = pygame.Surface((20, int(self.fuel / self.max_fuel * self.fuel_bar_height)))
            if self.fuel >= 70:
                self.image.fill((63, 153, 0))
            elif self.fuel >= 40:
                self.image.fill((255, 221, 0))
            else:
                self.image.fill((255, 0, 0))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y - int(self.fuel / self.max_fuel * self.fuel_bar_height)

    def refill(self, percent):
        self.fuel += self.max_fuel * (percent / 100)
        if self.fuel > self.max_fuel:
            self.fuel = self.max_fuel
