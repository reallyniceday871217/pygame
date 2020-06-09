import pygame
import sys
import random
from time import sleep

# screen size
padWidth = 480
padHeight = 640
rockImage = ['']  # rock image here

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter,  missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('shooting game')  # name of game
    background = pygame.image.load('')  # background image here
    fighter = pygame.image.load('')  # fighter image here
    missile = pygame.image.load('')  # missile image here
    explosion = pygame.image.load('')
    clock = pygame.time.Clock()

def runGame():
    global gamepad, clock, background, fighter, missile, explosion

    # size of fighter
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # initial position of fighter
    x = padwidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # list of missile coordinate
    missileXY = []

    # randomly select the rock and fall down
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # when missile shot the rock = True
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            # press the key and let fighter move
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_SPACE:
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    fighterX = 0

        drawObject(background, 0, 0)

        # let fighter do not move out the frame
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        drawObject(fighter, x, y)

        # draw missile on the screen
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                # when missile shot the rock
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
             for bx, by in missileXY:
                drawObject(missile, bx, by)

        rockY += rockSpeed

        # when rock hit the earth
        if rockY > padHeight:
            # new rock
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

        if isShot:
            drawObject(explosion, rockX, rockY)
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False
            
        drawObject(rock, rockX, rockY)

        pygame.display.update()

        clock.tick(60)  # set frames per second of game screen 60

    pygame.quit()

initGame()
runGame()

