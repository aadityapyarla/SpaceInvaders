import math
import pygame
import random
from pygame import mixer

# Initialized the game
pygame.init()
# Added Title, Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
# Background
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)
screen = pygame.display.set_mode((800, 600))
# Rocket
rocket_image = pygame.image.load("rocket.png")
rocketX = 370
rocketY = 480
rocketX_change = 0
# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
# Random respawns of enemies
for i in range(num_enemies):
    enemy_image.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
# Bullet
bullet_image = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def rocket(x, y):
    screen.blit(rocket_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance <= 27:
        return True
    else:
        return False


def rocket_crash(enemyx, enemyy, rocketx, rockety):
    distance = math.sqrt(math.pow(enemyx - rocketx, 2) + math.pow(enemyy - rockety, 2))
    if distance <= 35:
        return True
    else:
        return False


show_game_over = False
running = True
while running:
    try:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
    except KeyboardInterrupt:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rocketX_change = -5

            if event.key == pygame.K_RIGHT:
                rocketX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = rocketX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                rocketX_change = 0

    rocketX += rocketX_change
    if rocketX <= 0:
        rocketX = 0
    if rocketX >= 716:
        rocketX = 716

    game_over = False
    for i in range(num_enemies):
        rocket_blast = rocket_crash(enemyX[i], enemyY[i], rocketX, rocketY)
        if rocket_blast:
            for j in range(num_enemies):
                enemyY[j] = 2000
                game_over = True
                show_game_over = True

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
        if game_over is True:
            over_sound = mixer.Sound("gameover.wav")
            over_sound.play()
            break
    if show_game_over:
        game_over_text()
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    rocket(rocketX, rocketY)
    pygame.display.update()
