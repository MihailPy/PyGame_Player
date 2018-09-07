import random

import pygame

from settings import WIDTH, HEIGHT

class Plasmoid(pygame.sprite.Sprite):
    speed = -15

    def __init__(self, position):
        super(Plasmoid, self).__init__()

        self.image = pygame.image.load("assets/plasmoid.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
    def update(self):
        self.rect.move_ip((0, self.speed))

class Player(pygame.sprite.Sprite):
    max_speed = 10
    shooting_cooldoen = 150

    def __init__(self, clock, plasmoids):
        super(Player, self).__init__()

        self.clock = clock
        self.plasmoids = plasmoids

        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.current_speed = 0

        self.current_shooting_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.current_speed = -self.max_speed
        elif keys[pygame.K_RIGHT]:
            self.current_speed = +self.max_speed
        else:
            self.current_speed = 0

        self.rect.move_ip((self.current_speed, 0))

        self.process_shooting()

    def process_shooting(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
            self.plasmoids.add(Plasmoid(self.rect.midtop))
            self.current_shooting_cooldown = self.shooting_cooldoen
        else:
            self.current_shooting_cooldown -= self.clock.get_time()

        for plasmoid in list(self.plasmoids):
            if plasmoid.rect.bottom < 0:
                self.plasmoids.remove(plasmoid)

class Backgraund(pygame.sprite.Sprite):
    def __init__(self):
        super(Backgraund, self).__init__()

        self.image = pygame.image.load("assets/backgraund.png")
        self.rect = self.image.get_rect()

        self.rect.bottom = HEIGHT
    def update(self):
        self.rect.bottom += 5

        if self.rect.bottom >= self.rect.height:
            self.rect.bottom = HEIGHT

class Car(pygame.sprite.Sprite):
    cooldown = 1000
    current_cooldown = 0
    speed = 7
    def __init__(self):
        super(Car,self).__init__()
        p = [76, 200, 326]

        image_name = "assets/car{}.png".format(random.randint(1, 4))

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (p[random.randint(0, 2)], 0)

    def update(self):
        self.rect.move_ip((0, self.speed))

    @staticmethod
    def process_meteors(clock, meteorites):
        if Car.current_cooldown <= 0:
            meteorites.add(Car())
            Car.current_cooldown = Car.cooldown
        else:
            Car.current_cooldown -= clock.get_time()

        for m in list(meteorites):
            if (m.rect.right < 0 or m.rect.left > WIDTH or m.rect.top > HEIGHT):
                meteorites.remove(m)