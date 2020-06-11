import pygame
import sys
import random
from time import sleep
# screen size
padWidth = 480
padHeight = 640
rockImage = ['0.png', '1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png']  # rock image here


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def get_answer():
    """
    using module random
    get four-digit integer with all digits distinct
    first digit should not be zero
    """
    digit = '1234567890'
    first_digit = str(random.randint(1, 9))
    answer_list = random.sample(digit.replace(first_digit, ''), 3)
    answer = first_digit
    for num in answer_list:
        answer += num
    return answer


def random_digits():
    """
    produce 4 random digits
    """
    digit = '1234567890'
    digits = []
    for i in random.sample(digit, 4):
        digits.append(int(i))
    return digits


def AB(guess, answer):  # guess is a int
    """get a and b"""
    guess = str(guess)
    guess = list(guess)
    answer_list = list(answer)
    A_list = []
    B_list = []
    for i in range(len(answer_list)):
        # if digit location and number are same, get a
        if guess[i] == answer_list[i]:
            A_list.append(guess[i])
        # if digit number is in the answer but not the right location, get b
        else:
            if guess[i] in answer_list:
                B_list.append(guess[i])
    a = len(A_list)
    b = len(B_list)
    return a, b


def initGame():
    global gamepad, clock, background, fighter, missile, explosion, super, font
    pygame.init()
    gamepad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('shooting game')  # name of game
    background = pygame.image.load('white_background.jpg')  # background image here
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
    digits = random_digits()
    rock = pygame.image.load(rockImage[digits[0]])
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, 50)
    rockY = -random.randrange(0, 10)
    rockSpeed = 12
    # rock 1
    rock1 = pygame.image.load(rockImage[digits[1]])
    rock1X = random.randrange(100, 200)
    rock1Y = -random.randrange(0, 10)
    # rock 2
    rock2 = pygame.image.load(rockImage[digits[2]])
    rock2X = random.randrange(250, 300)
    rock2Y = -random.randrange(0, 10)
    # rock 3
    rock3 = pygame.image.load(rockImage[digits[3]])
    rock3X = random.randrange(350, 400)
    rock3Y = -random.randrange(0, 10)

    star = pygame.image.load('star.png')
    starSpeed = 30

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
    answer = get_answer()
    guess = ""
    guess_time = 0
    guess_list = []
    a_list = []
    b_list = []
    invalid = False
    ab = False
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
                bxy[1] -= 20
                missileXY[i][1] = bxy[1]

                # when missile shot the rock
                if bxy[1] < rockY:
                    if rockX < bxy[0] < rockX + rockWidth:
                        if not rock_isShot:
                            missileXY.remove(bxy)
                            rock_isShot = True
                            shotCount += 1
                            guess += str(digits[0])
                            number = digits[0]
                if bxy[1] < rock1Y:
                    if rock1X < bxy[0] < rock1X + rockWidth:
                        if not rock_isShot:
                            missileXY.remove(bxy)
                            rock_isShot = True
                            shotCount += 1
                            guess += str(digits[1])
                            number = digits[1]
                if bxy[1] < rock2Y:
                    if rock2X < bxy[0] < rock2X + rockWidth:
                        if not rock_isShot:
                            missileXY.remove(bxy)
                            rock_isShot = True
                            shotCount += 1
                            guess += str(digits[2])
                            number = digits[2]
                if bxy[1] < rock3Y:
                    if rock3X < bxy[0] < rock3X + rockWidth:
                        if not rock_isShot:
                            missileXY.remove(bxy)
                            rock_isShot = True
                            shotCount += 1
                            guess += str(digits[3])
                            number = digits[3]

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
        rock1Y += rockSpeed
        rock2Y += rockSpeed
        rock3Y += rockSpeed

        if star_exist is True:
            starY += starSpeed

        # when rock hit the earth
        if rockY > padHeight:
            # new rock
            num = random.randint(0, 9)
            while num in digits:
                num = random.randint(0, 9)
            digits[0] = num
            rock = pygame.image.load(rockImage[digits[0]])
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = -random.randrange(0, 10)
        if rock1Y > padHeight:
            # new rock
            num = random.randint(0, 9)
            while num in digits:
                num = random.randint(0, 9)
            digits[1] = num
            rock1 = pygame.image.load(rockImage[digits[1]])
            rock1X = random.randrange(0, padWidth - rockWidth)
            rock1Y = -random.randrange(0, 10)
        if rock2Y > padHeight:
            # new rock
            num = random.randint(0, 9)
            while num in digits:
                num = random.randint(0, 9)
            digits[2] = num
            rock2 = pygame.image.load(rockImage[digits[2]])
            rock2X = random.randrange(0, padWidth - rockWidth)
            rock2Y = -random.randrange(0, 10)
        if rock3Y > padHeight:
            # new rock
            num = random.randint(0, 9)
            while num in digits:
                num = random.randint(0, 9)
            digits[3] = num
            rock3 = pygame.image.load(rockImage[digits[3]])
            rock3X = random.randrange(0, padWidth - rockWidth)
            rock3Y = -random.randrange(0, 10)

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
            if starY > y:
                if x < starX < x + fighterWidth and super_mode is False:
                    super_mode = True
                    starX = 0
                    starY = -100
                    super_begin = time
                    star_exist = False
                    guess += answer[len(guess)]
                    pygame.time.wait(500)

        # super mode last for 5 sec
        if super_mode:
            if time - super_begin >= 5000:
                super_mode = False

        if rock_isShot:
            if number == digits[0]:
                drawObject(explosion, rockX, rockY)
                num = random.randint(0, 9)
                while num in digits:
                    num = random.randint(0, 9)
                digits[0] = num
                rock = pygame.image.load(rockImage[digits[0]])
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = -random.randrange(0, 10)
                rock_isShot = False
            if number == digits[1]:
                drawObject(explosion, rock1X, rock1Y)
                num = random.randint(0, 9)
                while num in digits:
                    num = random.randint(0, 9)
                digits[1] = num
                rock1 = pygame.image.load(rockImage[digits[1]])
                rock1X = random.randrange(0, padWidth - rockWidth)
                rock1Y = -random.randrange(0, 10)
                rock_isShot = False
            if number == digits[2]:
                drawObject(explosion, rock2X, rock2Y)
                num = random.randint(0, 9)
                while num in digits:
                    num = random.randint(0, 9)
                digits[2] = num
                rock2 = pygame.image.load(rockImage[digits[2]])
                rock2X = random.randrange(0, padWidth - rockWidth)
                rock2Y = -random.randrange(0, 10)
                rock_isShot = False
            if number == digits[3]:
                drawObject(explosion, rock3X, rock3Y)
                num = random.randint(0, 9)
                while num in digits:
                    num = random.randint(0, 9)
                digits[3] = num
                rock3 = pygame.image.load(rockImage[digits[3]])
                rock3X = random.randrange(0, padWidth - rockWidth)
                rock3Y = -random.randrange(0, 10)
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
        drawObject(rock1, rock1X, rock1Y)
        drawObject(rock2, rock2X, rock2Y)
        drawObject(rock3, rock3X, rock3Y)

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

        # show the score
        score = 2 * shotCount - 3 * rockPassed
        color = (0, 0, 0)
        guess_text = font.render("Guess: " + str(guess), True, color)
        history_text = font.render("History: ", True, color)
        answer_text = font.render("Answer: " + str(answer), True, color)
        gamepad.blit(guess_text, (0, 0))
        gamepad.blit(history_text, (0, 20))
        gamepad.blit(answer_text, (0, 300))
        if len(guess) == 4:
            number_guess = guess
            guess = int(guess)
            guess_digits = set(str(guess))
            if 1000 <= guess <= 9999 and len(guess_digits) == 4:
                guess_time += 1
                guess_list.append(number_guess)
                a, b = AB(guess, answer)
                a_list.append(a)
                b_list.append(b)
                ab = True
            else:
                invalid = True
                invalid_time = time
            guess = ""
        if invalid:
            invalid_text = font.render(number_guess + " is invalid, try again", True, color)
            gamepad.blit(invalid_text, (padWidth * 0.2, 400))
            if time - invalid_time >= 3000:
                invalid = False
        if ab:
            ab_text = []
            for k in range(guess_time):
                ab_text.append(font.render(guess_list[k] + " = " + str(a_list[k]) + "a" + str(b_list[k]) + "b", True, color))
                gamepad.blit(ab_text[k], (0, 40 + 20 * k))
        pygame.display.update()
        if a_list:
            if a_list[-1] == 4:
                white = (255, 255, 255)
                gamepad.fill(white)
                gameover_text = font.render('Congratulation! The final answer is ' + answer + ".", True, color)
                gamepad.blit(gameover_text, (5, 250))
                pygame.display.update()

        clock.tick(60)  # set frames per second of game screen 60
    pygame.quit()


initGame()
runGame()
