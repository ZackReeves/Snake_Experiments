import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

sw = 800
sh = 600

head_img = pygame.image.load("img/snakehead.png")
apple_img = pygame.image.load("img/apple.png")
icon = pygame.image.load("img/icon.png")

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

fps = 15

block_size = 20
apple_thickness = block_size

font_s = pygame.font.SysFont("comicsansms", 25)
font_m = pygame.font.SysFont("comicsansms", 30)
font_l = pygame.font.SysFont("comicsansms", 50)

direction = "right"


def game_start():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(white)
        msg_to_screen("Welcome to Snake!", green, -100, "large")
        msg_to_screen("Objective: EAT THE APPLES", black, -30, "small")
        msg_to_screen("The more you eat, the longer you get,", black, 10, "small")
        msg_to_screen("don't tie yourself in a knot though!", black, 50, "small")
        msg_to_screen("Press SPACE to play, P to pause or Q to quit.", black, 180, "small")

        pygame.display.update()
        clock.tick(fps)


def pause():

    paused = True

    msg_to_screen("Paused!", black, -100, "large")
    msg_to_screen("Press SPACE to continue or Q to quit.", black, 25)
    pygame.display.update()

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(fps)


def score(points):
    text = text_objects("Score: " + str(points), black, "small")
    screen.blit(text[0], (0, 0))


def apple_gen():
    apple_x = round(random.randrange(0, sw - block_size) / block_size) * block_size
    apple_y = round(random.randrange(0, sh - block_size) / block_size) * block_size

    return apple_x, apple_y


def snake(snake_list):

    if direction == "right":
        head = pygame.transform.rotate(head_img, 270)
    elif direction == "down":
        head = pygame.transform.rotate(head_img, 180)
    elif direction == "left":
        head = pygame.transform.rotate(head_img, 90)
    else:
        head = head_img

    for XnY in snake_list[:-1]:
        pygame.draw.rect(screen, green, [XnY[0], XnY[1], block_size, block_size])

    screen.blit(head, (snake_list[-1][0], snake_list[-1][1]))


def text_objects(text, colour, size):

    if size == "med":
        txt_surf = font_m.render(text, True, colour)
    elif size == "large":
        txt_surf = font_l.render(text, True, colour)
    else:
        txt_surf = font_s.render(text, True, colour)

    return txt_surf, txt_surf.get_rect()


def msg_to_screen(msg, colour, y_displace=0, size="small"):

    txt_surf, txt_rect = text_objects(msg, colour, size)
    txt_rect.center = sw//2, (sh//2) + y_displace
    screen.blit(txt_surf, txt_rect)


def game_loop():

    loop = True
    game_over = False

    global direction
    direction = "right"

    head_x = sw // 2
    head_y = sh // 2

    x_change = block_size
    y_change = 0

    snake_list = []
    snake_length = 1

    apple_x, apple_y = apple_gen()

    while loop:

        if game_over:
            msg_to_screen("Game over!", red, y_displace=-50, size="large")
            msg_to_screen("Press SPACE to play again or Q to quit", black, size="med")
            pygame.display.update()

        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        loop = False
                    if event.key == pygame.K_SPACE:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    x_change = -block_size
                    y_change = 0
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                    x_change = block_size
                    y_change = 0
                if event.key == pygame.K_UP:
                    direction = "up"
                    y_change = -block_size
                    x_change = 0
                if event.key == pygame.K_DOWN:
                    direction = "down"
                    y_change = block_size
                    x_change = 0
                if event.key == pygame.K_p:
                    pause()

        head_x += x_change
        head_y += y_change

        if head_x >= sw or head_x < 0 or head_y >= sh or head_y < 0:
            # game_over = True
            if head_x >= sw:
                head_x -= sw
            elif head_x < 0:
                head_x += sw
            if head_y >= sh:
                head_y -= sh
            elif head_y < 0:
                head_y += sh

        snake_head = [head_x, head_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        if head_x == apple_x and head_y == apple_y:
            apple_x, apple_y = apple_gen()
            snake_length += 1

        screen.fill(white)
        screen.blit(apple_img, (apple_x, apple_y))
        snake(snake_list)
        score(snake_length-1)

        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()


game_start()

game_loop()
