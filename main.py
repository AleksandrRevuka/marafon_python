import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from random import randint


def create_bonus():
    bonus = pygame.image.load('img/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(randint(0, width), -300, *bonus.get_size())
    bonus_speed = randint(1, 2)
    return [bonus, bonus_rect, bonus_speed]


def create_enemy():
    enemy = pygame.image.load('img/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, randint(0, height), *enemy.get_size())
    enemy_speed = randint(2, 4)
    return [enemy, enemy_rect, enemy_speed]


def control_player(pressed_keys, player_rect, player_speed):
    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    return pressed_keys, player_rect, player_speed


def move_enemy(is_working, enemies, player_rect):
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -200:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    return is_working, enemies, player_rect


def move_bonus(bonuses, player_rect, scores):
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height + 50:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
    return bonuses, player_rect, scores


def main():
    bg = pygame.transform.scale(pygame.image.load('img/background.png').convert(), screen)
    bg_x = 0
    bg_x2 = bg.get_width()
    bg_speed = 3

    player = pygame.image.load('img/player.png').convert_alpha()
    player_rect = player.get_rect()
    player_speed = 5

    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 9000)

    font = pygame.font.SysFont("Verdana", 20)

    is_working = True
    enemies = []
    bonuses = []
    scores = 0
    while is_working:

        FPS.tick(50)

        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = False

            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

        pressed_keys = pygame.key.get_pressed()

        bg_x -= bg_speed
        bg_x2 -= bg_speed

        if bg_x < -bg.get_width():
            bg_x = bg.get_width()

        if bg_x2 < - bg.get_width():
            bg_x2 = bg.get_width()

        main_surface.blit(bg, (bg_x, 0))
        main_surface.blit(bg, (bg_x2, 0))
        main_surface.blit(player, player_rect)
        main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))

        is_working, enemies, player_rect = move_enemy(is_working, enemies, player_rect)
        bonuses, player_rect, scores = move_bonus(bonuses, player_rect, scores)
        pressed_keys, player_rect, player_speed = control_player(pressed_keys, player_rect, player_speed)

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    FPS = pygame.time.Clock()
    screen = width, height = 800, 600
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    main_surface = pygame.display.set_mode(screen)
    main()
