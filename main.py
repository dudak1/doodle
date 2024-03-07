import pygame
import sys
import random
import os


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


pygame.init()

WIDTH, HEIGHT = 400, 550
dy = 0
h = 200
score = 0
best = score
clock = pygame.time.Clock()

BG = pygame.image.load(resource_path('multimedia/background.png'))
CHAR = pygame.image.load(resource_path('multimedia/char.png'))
CHAR = pygame.transform.scale(CHAR, (100, 100))
PLAT = pygame.image.load(resource_path('multimedia/plat.png'))
PLAT = pygame.transform.scale(PLAT, (75, 25))
KILL = pygame.image.load(resource_path('multimedia/kill.png'))
KILL = pygame.transform.scale(KILL, (75, 25))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Doodle Jump')

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 30)

fall_sound = pygame.mixer.Sound(resource_path("multimedia/fall.wav"))
jump_sound = pygame.mixer.Sound(resource_path("multimedia/jump.mp3"))
death_sound = pygame.mixer.Sound(resource_path("multimedia/death.wav"))


class Plat:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Char:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Kill:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generate_field():
    platforms = []
    coordinates_x = []
    coordinates_y = []
    for i in range(9):
        x, y = random.randrange(0, WIDTH), random.randrange(0, HEIGHT)
        coordinates_x_mod = list(map(lambda c: list(range(c - 75, c + 75)), coordinates_x))
        coordinates_y_mod = list(map(lambda c: list(range(c - 25, c + 25)), coordinates_y))
        while any(map(lambda a: x in a, coordinates_x_mod)) and any(map(lambda a: y in a, coordinates_y_mod)):
            x, y = random.randrange(0, WIDTH), random.randrange(0, HEIGHT)
        coordinates_x += [x]
        coordinates_y += [y]
        platforms.append(Plat(x, y))
    platforms.append(Kill(random.randrange(0, WIDTH), random.randrange(0, HEIGHT)))
    return platforms


platforms = generate_field()

char = Char(100, 50)

running = True
placement = True
char_view = 'right'
cur_view = CHAR
directions = {"right": False, "left": False}
pause = False
death = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and not death and not pause:
            if event.key == pygame.K_RIGHT:
                directions['right'] = True
                if char_view != 'right':
                    cur_view = CHAR
                    char_view = 'right'
            elif event.key == pygame.K_LEFT:
                directions['left'] = True
                if char_view != 'left':
                    cur_view = pygame.transform.flip(CHAR, True, False)
                    char_view = 'left'
            elif event.key == pygame.K_ESCAPE:
                pause = not pause

        if event.type == pygame.KEYUP and not death and not pause:
            if event.key == pygame.K_RIGHT:
                directions['right'] = False
            elif event.key == pygame.K_LEFT:
                directions['left'] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (pause or death):
                x, y = event.pos
                if 100 < x < 300:
                    if 138 < y < 208 and pause:
                        pause = not pause
                    elif 238 < y < 308:
                        score = 0
                        platforms = generate_field()
                        pause = False
                        death = False
                        char = Char(100, 100)
                    elif 338 < y < 408:
                        sys.exit()

    if not pause and not death:
        if directions['right']:
            char.x += 5
        if directions['left']:
            char.x -= 5
        if char.x > WIDTH:
            char.x -= WIDTH
        if char.x < -100:
            char.x += WIDTH

        if char.y < h:
            char.y = h
            for platform in platforms:
                platform.y -= dy
                if platform.y > HEIGHT:
                    platform.y = 0
                    platform.x = random.randrange(0, WIDTH)
                    score += 1

        dy += 0.3
        char.y += dy
        if char.y > HEIGHT:
            death = True
            fall_sound.play()

        for platform in platforms:
            if (char.x + 60 > platform.x) and (char.x + 20 < platform.x + 75) and (char.y + 70 > platform.y) and (char.y + 70 < platform.y + 25) and dy > 0:
                if isinstance(platform, Plat):
                    dy = -10
                    jump_sound.play()
                else:
                    death = True
                    death_sound.play()
    screen.blit(BG, (0, 0))

    for platform in platforms:
        if isinstance(platform, Kill):
            screen.blit(KILL, (platform.x, platform.y))
        else:
            screen.blit(PLAT, (platform.x, platform.y))

    text = FONT.render('Счёт: ' + str(score), 1, (0, 0, 0))
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))

    screen.blit(cur_view, (char.x, char.y))

    if pause:
        continue_button = pygame.draw.rect(screen, (214, 146, 73), (100, 138, 200, 70), border_radius=20)
        restart_button = pygame.draw.rect(screen, (214, 146, 73), (100, 238, 200, 70), border_radius=20)
        exit_button = pygame.draw.rect(screen, (214, 146, 73), (100, 338, 200, 70), border_radius=20)
        continue_text = FONT.render('Продолжить', 1, (0, 0, 0))
        restart_text = FONT.render('Перезапуск', 1, (0, 0, 0))
        exit_text = FONT.render('Выйти', 1, (0, 0, 0))
        screen.blit(continue_text, (107, 150))
        screen.blit(restart_text, (117, 250))
        screen.blit(exit_text, (150, 350))
    if death:
        restart_button = pygame.draw.rect(screen, (214, 146, 73), (100, 238, 200, 70), border_radius=20)
        exit_button = pygame.draw.rect(screen, (214, 146, 73), (100, 338, 200, 70), border_radius=20)
        restart_text = FONT.render('Перезапуск', 1, (0, 0, 0))
        exit_text = FONT.render('Выйти', 1, (0, 0, 0))
        if best < score:
            rec_text = FONT.render('Новый рекорд! - ' + str(score), 1, (0, 0, 0))
            screen.blit(rec_text, (80, 170))
        else:
            rec_text = FONT.render('Рекорд: ' + str(best),  1, (0, 0, 0))
            screen.blit(rec_text, (135, 150))
        screen.blit(restart_text, (117, 250))
        screen.blit(exit_text, (150, 350))
    clock.tick(60)
    pygame.display.flip()
