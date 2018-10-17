import random, time
import pygame

from settings import WIDTH, HEIGHT

#class Button(pygame.sprite.Sprite):


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
    plasm = 15
    max_speed = 10
    shooting_cooldoen = 150

    def __init__(self, clock, plasmoids):
        super(Player, self).__init__()

        self.clock = clock
        self.plasmoids = plasmoids


        self.texture = pygame.image.load("assets/PlayerA.png")
        #spritesheet = pygame.image.load("assets/PlayerA.png")

        self.image = self.texture.subsurface(pygame.Rect(899, 110, 74, 74))
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.current_speed = 0

        self.current_shooting_cooldown = 0

        self.flip = []
        self.flip.append(self.texture.subsurface(pygame.Rect(814, 109, 74, 74)))
        self.flip.append(self.texture.subsurface(pygame.Rect(733, 109, 74, 76)))
        self.flip.append(self.texture.subsurface(pygame.Rect(655, 109, 73, 77)))
        self.flip.append(self.texture.subsurface(pygame.Rect(576, 104, 69, 79)))
        self.flip.append(self.texture.subsurface(pygame.Rect(501, 102, 64, 81)))
        self.flip.append(self.texture.subsurface(pygame.Rect(444, 99, 54, 85)))
        self.flip.append(self.texture.subsurface(pygame.Rect(402, 96, 33, 88)))
        self.flip.append(self.texture.subsurface(pygame.Rect(369, 94, 22, 91)))
        self.flip.append(self.texture.subsurface(pygame.Rect(343, 95, 11, 91)))
        self.flip.append(self.texture.subsurface(pygame.Rect(302, 95, 28, 89)))
        self.flip.append(self.texture.subsurface(pygame.Rect(243, 98, 42, 87)))
        self.flip.append(self.texture.subsurface(pygame.Rect(176, 104, 58, 81)))
        self.flip.append(self.texture.subsurface(pygame.Rect(98, 107, 67, 67)))
        self.flip.append(self.texture.subsurface(pygame.Rect(16, 110, 73, 73)))
        self.flip.append(self.texture.subsurface(pygame.Rect(895, 22, 71, 74)))
        self.flip.append(self.texture.subsurface(pygame.Rect(812, 20, 73, 71)))
        self.flip.append(self.texture.subsurface(pygame.Rect(737, 18, 67, 76)))
        self.flip.append(self.texture.subsurface(pygame.Rect(673, 13, 57, 80)))
        self.flip.append(self.texture.subsurface(pygame.Rect(919, 10, 44, 85)))
        self.flip.append(self.texture.subsurface(pygame.Rect(579, 4, 23, 89)))
        self.flip.append(self.texture.subsurface(pygame.Rect(547, 3, 12, 90)))
        self.flip.append(self.texture.subsurface(pygame.Rect(515, 4, 21, 90)))
        self.flip.append(self.texture.subsurface(pygame.Rect(464, 7, 39, 87)))
        self.flip.append(self.texture.subsurface(pygame.Rect(404, 9, 54, 84)))
        self.flip.append(self.texture.subsurface(pygame.Rect(335, 11, 64, 82)))
        self.flip.append(self.texture.subsurface(pygame.Rect(260, 14, 71, 80)))
        self.flip.append(self.texture.subsurface(pygame.Rect(182, 16, 74, 77)))
        self.flip.append(self.texture.subsurface(pygame.Rect(104, 18, 74, 75)))
        self.flip.append(self.texture.subsurface(pygame.Rect(14, 20, 75, 73)))
        self.f = 0
    def update(self):
        def flipR():
            print (self.f)
            self.current_speed = +self.max_speed - 5
            self.image = self.flip[self.f]
            if self.f == len(self.flip) - 1:
                self.f = 0
            else:
                self.f += 1
        if self.rect.centerx > 365:
            self.rect.centerx = 367
        elif self.rect.centerx < 30:
            self.rect.centerx = 32
        def flipL():
            print(len(self.flip))
            print (self.f)
            self.current_speed = -self.max_speed + 5
            self.image = self.flip[self.f]
            if self.f == -29:
                self.f = 0
            else:
                self.f -= 1

        keys = pygame.key.get_pressed()


        if keys[pygame.K_LEFT]:
            self.current_speed = -self.max_speed
            self.image = self.texture.subsurface(pygame.Rect(103, 20, 75, 75))
        elif keys[pygame.K_RIGHT]:
            self.current_speed = +self.max_speed
            self.image = self.texture.subsurface(pygame.Rect(735, 110, 75, 75))
        elif keys[pygame.K_d]:
            flipR()
        elif keys[pygame.K_a]:
            flipL()
        else:
            self.image = self.texture.subsurface(pygame.Rect(898, 110, 75, 75))
            self.current_speed = 0


        self.rect.move_ip((self.current_speed, 0))

        self.process_shooting()

    def process_shooting(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
            if self.plasm < 1:
                return

            self.plasm -= 1
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

        self.image = pygame.image.load(image_name).subsurface(pygame.Rect(6, 3, 68, 111))
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
