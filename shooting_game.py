import pygame
import sys
import random
from time import sleep

# screen size
padWidth = 480
padHeight = 640
rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', 'rock06.png', 'rock07.png']  # rock image here


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def initGame():
    global gamepad, clock, background, fighter, missile, explosion, super, font
    pygame.init()
    gamepad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('shooting game')  # name of game
    background = pygame.image.load('background.png')  # background image here
    fighter = pygame.image.load('fighter.png')  # fighter image here
    missile = pygame.image.load('missile.png')  # missile image here
    explosion = pygame.image.load('explosion.png')
    super = pygame.image.load('sun.png')
    clock = pygame.time.Clock()
    font = pygame.font.Font('NanumGothic.ttf', 24)


def runGame():
    global gamepad, clock, background, fighter, missile, explosion, super, font
    # size of fighter
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # initial position of fighter
    x = padWidth * 0.45
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
    rockSpeed = 10

    star = pygame.image.load('star.png')
    starSpeed = 20

    # when missile shot the rock or star = True
    rock_isShot = False
    star_isShot = False
    fighter_isCrash = False
    shotCount = 0
    rockPassed = 0
    score = 0
    # star does not exist until 5sec
    star_exist = False
    # the fighter get into super_mode for 5 sec after eating star
    super_mode = False

    onGame = False
    while not onGame:
        time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            # press the key and let fighter move
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_RIGHT:
                    fighterX += 15

                elif event.key == pygame.K_LEFT:
                    fighterX -= 15

                elif event.key == pygame.K_SPACE:
                    missileX = x + fighterWidth / 2
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
                    if rockX < bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        rock_isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

                # when missile shot the star
                if star_exist:
                    if bxy[1] < starY:
                        if starX < bxy[0] < starX + starWidth:
                            missileXY.remove(bxy)
                            star_isShot = True

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        rockY += rockSpeed
        if star_exist is True:
            starY += starSpeed

        # when rock hit the earth
        if rockY > padHeight:
            # new rock
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # when star hit the earth
        if star_exist:
            if starY > padHeight:
                star_exist = False

        # when rock hit the fighter
        if rockY >= y:
            # super mode fighter crash the rock
            if rockX < x < rockX + rockWidth and not super_mode:
                fighter_isCrash = True
            elif rockX < x < rockX + rockWidth and super_mode:
                shotCount += 1
                rock_isShot = True

        # when fighter eat the star
        if star_exist:
            if starY >= y:
                if x <= starX <= x + fighterWidth:
                    super_mode = True
                    super_begin = time

        # super mode last for 5 sec
        if super_mode is True:
            if time - super_begin >= 5000:
                super_mode = False

        if rock_isShot:
            drawObject(explosion, rockX, rockY)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rock_isShot = False

        if star_isShot:
            drawObject(explosion, starX, starY)
            starSize = star.get_rect().size
            starWidth = starSize[0]
            starHeight = starSize[1]
            starX = random.randrange(0, padWidth - starWidth)
            starY = 0
            star_exist = False
            star_isShot = False

        if fighter_isCrash:
            drawObject(explosion, x - 10, y)
            fighter_isCrash = False

        drawObject(rock, rockX, rockY)
        if star_exist:
            drawObject(star, starX, starY)

        if super_mode:
            drawObject(super, x - 2, y)

        if time >= 5000 and (time % 5000 <= 100) and star_exist is False and not super_mode:
            # print('draw star')
            starSize = star.get_rect().size
            starWidth = starSize[0]
            starHeight = starSize[1]
            starX = random.randrange(0, padWidth - starWidth)
            starY = 0
            star_exist = True
            # drawObject(star, starX, starY)

        # show the score
        score = 2 * shotCount - 3 * rockPassed
        white = (255, 255, 255)
        score_text = font.render("Score : " + str(score), True, white)
        shotCount_text = font.render("Shot Count : " + str(shotCount), True, white)
        rockPassed_text = font.render("Rock Passed : " + str(rockPassed), True, white)
        gamepad.blit(score_text, (0, 0))
        gamepad.blit(shotCount_text, (0, 20))
        gamepad.blit(rockPassed_text, (0, 40))

        pygame.display.update()
        clock.tick(60)  # set frames per second of game screen 60
    pygame.quit()


initGame()
runGame()
