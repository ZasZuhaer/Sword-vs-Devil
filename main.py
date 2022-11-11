import random
import pygame
import math

# initializing pygame
pygame.init()
# defining screen size of gui
screen = pygame.display.set_mode((800, 600))
# title and icon import
pygame.display.set_caption("Magic Sword")
icon = pygame.image.load('sword.png')
pygame.display.set_icon(icon)

# player, enemies, bullet and images
playerImg = pygame.image.load('sizedsword.png')
enemyImg = pygame.image.load('sizeddevil.png')
bulletImg = pygame.image.load('bulsword.png')
playerX, playerY = 370, 520  # player default coordinates
enemyx, enemyy = 0, 0  # initializing the enemy coordinates but will be randomized in the loop
bulx, buly = 1000, 1000  # initializing but will be specified when space is pressed


# function to spawn player
def spawn_player(x, y):
    screen.blit(playerImg, (x, y))


# function to draw enemy image
def draw_enemy(x, y):
    screen.blit(enemyImg, (x, y))  # enemy random spawning cords


# function to spawn enemy at random coordinates
# assign the returned value as enemyx and enemyy when spawned, to use the variables in the loop to change it as needed
def spawn_enemy(px, py):
    px += 25
    py += 25
    while True:
        x, y = random.randint(0, 750), random.randint(0, 550)
        x += 30
        y += 30
        distance = math.sqrt(pow(x - px, 2) + pow(y - py, 2))
        if distance < 250:
            continue
        else:
            break
    draw_enemy(x, y)
    return x, y


# function to draw bullet
def draw_bullet(x, y):
    screen.blit(bulletImg, (x, y))


# checking if the player or enemy reached the edge of screen
def stop_at_edge(x, y):
    if x < 0:
        x = 0
    if x > 750:
        x = 750
    if y < 0:
        y = 0
    if y > 550:
        y = 550
    return x, y


def bul_reach_edge(x, y):
    if x < 0 or x > 750 or y < 0 or y > 550:
        return True
    else:
        return False


# function to check if the player hits the enemy
# here we used linear difference equation to return killed value true, if the distance is less than a certain length
def enemy_hit(px, py, ex, ey):
    px += 25
    py += 25
    ex += 30
    ey += 30
    distance = math.sqrt(pow(ex-px, 2) + pow(ey-py, 2))
    if distance < 45:
        return True
    else:
        return False


def shot_hit(sx, sy, ex, ey):
    sx += 12.5
    sy += 12.5
    ex += 25
    ey += 25
    distance = math.sqrt(pow(ex - sx, 2) + pow(ey - sy, 2))
    if distance < 40:
        return True
    else:
        return False


# function to get the devil closer to sword and get the change of devils cords
def get_closer(px, py, ex, ey):
    cox, coy = 0, 0
    if px > ex:
        cox = 0.10
    elif px < ex:
        cox = -0.10
    if py > ey:
        coy = 0.10
    elif py < ey:
        coy = -0.10
    return cox, coy


# defining running cases
playing = True  # at the initiation playing value will be true
killed = True  # assuming when the game started the devil was killed, so it needs to be spawned in the loop
count = 0  # counting the numbers of devils killed
space = False
shooting = False
bul_edge_reach = False
bxc, byc = 0, 0
lost = False
which = 'none'

while playing:

    # variables to move the enemy and player from the place its spawned
    echangex, echangey = 0, 0  # set 0, 0 everytime so enemy moves only once in each loop
    xchange, ychange = 0, 0  # set 0, 0 everytime so enemy moves only once in each key press

    # setting the background color
    screen.fill((0, 0, 0))

    # event checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # closing the window if close button is pressed
            playing = False

    if lost:
        break

    # checking if any keys are pressed
    # this block detects multiple key presses and move the player and enemy accordingly in multiple directions together
    # each key press player moves 0.25 pixels and devil moves 0.10 pixels
    # when keys are released nobody moves
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        xchange = 0.25
        which = 'right'
    if keys[pygame.K_LEFT]:
        xchange = -0.25
        which = 'left'
    if keys[pygame.K_UP]:
        ychange = -0.25
        which = 'up'
    if keys[pygame.K_DOWN]:
        ychange = 0.25
        which = 'down'

    if keys[pygame.K_SPACE]:
        bulx, buly = playerX+25-12.5, playerY+25-12.5
        if which == 'left':
            bxc, byc = -1, 0
        elif which == 'right':
            bxc, byc = 1, 0
        elif which == 'down':
            bxc, byc = 0, 1
        elif which == 'up':
            bxc, byc = 0, -1
        space = False
        shooting = True

    # getting the change of enemy cords
    echangex, echangey = get_closer(playerX, playerY, enemyx, enemyy)

    # assigning the changes of cords
    playerX += xchange
    playerY += ychange
    enemyx += echangex
    enemyy += echangey

    playerX, playerY = stop_at_edge(playerX, playerY)  # stopping the player to go through the edge of screen
    spawn_player(playerX, playerY)  # drawing the player

    if killed:  # checking if my enemy was killed then spawn at a new random coordinate
        enemyx, enemyy = spawn_enemy(playerX, playerY)
        killed = False  # reassigning the killed value after spawning to make it available to be killed again
    else:  # if not killed then keep drawing the enemy after updating its changed coordinates according to key press
        draw_enemy(enemyx, enemyy)

    # checking if the enemy was hit by sword
    if enemy_hit(playerX, playerY, enemyx, enemyy):
        lost = False

    if shot_hit(bulx, buly, enemyx, enemyy):
        killed = True
        shooting = False
        bulx, buly = 1000, 1000
        count += 1
        print(count)

    if shooting and not killed and not bul_reach_edge(bulx, buly):
        draw_bullet(bulx, buly)
        bulx += bxc
        buly += byc

    # updating the display with new coordinates of enemy/devil and player/sword
    pygame.display.update()
