import sys, pygame

from geme_objects import Player, Backgraund, Plasmoid, Car
from settings import SIZE, COLOR

pygame.init()
pygame.display.set_caption(", Worold!")

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
life = 15
r = 0
record = 0

backgaund = Backgraund()
all_objects = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
car = pygame.sprite.Group()
player = Player(clock, plasmoids)

all_objects.add(backgaund)
all_objects.add(player)
#all_objects.add(Car())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(COLOR)

    Car.process_meteors(clock, car)

    all_objects.update()
    plasmoids.update()
    car.update()

    pygame.sprite.groupcollide(car, plasmoids, True,True)

    player_and_meteors_collided = pygame.sprite.spritecollide(player, car, True)

    if player_and_meteors_collided:
        life = life - 1
        r = 0
    if life < 1:
        r = 1
        all_objects.remove(player)
    if r == 0:
        record = record + 1 % 3


    all_objects.draw(screen)
    plasmoids.draw(screen)

    car.draw(screen)
    font = pygame.font.Font(None, 25)
    life = int(life)
    text = font.render("Жизнь: " + str(life),True,(255,255,255))
    text1 = font.render("Time: " + str(record),True,(255,255,255))
    screen.blit(text, [15, 15])
    screen.blit(text1, [15,30])

    pygame.display.flip()
    clock.tick(30)