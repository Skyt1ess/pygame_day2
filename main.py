import random, time

import pygame

pygame.init()

display_size = [600, 900]

display = pygame.display.set_mode(display_size)

background = pygame.image.load('C:/Users/Islam/Desktop/pygame/day2/assets/background-day.png')
background = pygame.transform.scale(background, display_size)
background_x = 0
background_speed = -0.2
game = True
end = False

base = pygame.image.load('assets/base.png')
base = pygame.transform.scale(base, (display_size[0], base.get_height()))
base_speed = -2
base_x = 0
base_y = display_size[1] - base.get_height()


bird_downflap = pygame.image.load('assets/redbird-downflap.png')
bird_midflap = pygame.image.load('assets/redbird-midflap.png')
bird_upflap = pygame.image.load('assets/redbird-upflap.png')

bird_animation = [bird_midflap, bird_downflap, bird_midflap, bird_upflap]

for i in range(len(bird_animation)):
    bird_animation[i] = pygame.transform.scale2x(bird_animation[i])


bird_img = bird_animation[0]
bird_ind = 0
bird_x = 50
bird_y = display_size[1] / 2 - bird_img.get_height() / 2

gravity = 0.1
bird_move_y = 0
jump = -4

score = 0
high_score = 0

font = pygame.font.Font('04B_19.TTF', 32)
hihg_score_font = pygame.font.Font('04B_19.TTF', 64)
restart_font = pygame.font.SysFont('None', 48)

BIRDFLAP = pygame.USEREVENT + 0
pygame.time.set_timer(BIRDFLAP, 150)


pipe_img = pygame.image.load('assets/pipe-green.png')
pipe_img = pygame.transform.scale(pipe_img, (pipe_img.get_width() * 1.25, pipe_img.get_height()))
pipe_img_reverse = pygame.transform.rotate(pipe_img, 180)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT + 1
spawn_speed = 1200
pipe_speed = base_speed
pipe_dist = 200

pygame.time.set_timer(SPAWNPIPE, spawn_speed)

sound_hit = pygame.mixer.Sound('sound/sfx_hit.wav')
sound_hit.set_volume(0.5)

sound_die = pygame.mixer.Sound('sound/sfx_die.wav')
sound_die.set_volume(0.5)

sound_wing = pygame.mixer.Sound('sound/sfx_wing.wav')
sound_die.set_volume(0.5)

sound_point = pygame.mixer.Sound('sound/sfx_point.wav')
sound_die.set_volume(0.5)


def score_display():
    score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    display.blit(score_surface, (10, 10))

    if not game:
        restart_surface = restart_font.render("Press space to restart" , True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(display_size[0] / 2, display_size[1] / 2))
        display.blit(restart_surface, restart_rect)

        high_score_surface = hihg_score_font.render("High Score: " + str(high_score), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(display_size[0] / 2, display_size[1] / 2 - 100))
        display.blit(high_score_surface, high_score_rect)





def isCollision(X1, Y1, Img1, X2, Y2, Img2):
    delta = 18
    first = pygame.Rect(X1, Y1, Img1.get_width(), Img1.get_height())
    second = pygame.Rect(X2 + delta, Y2 + delta, Img2.get_width() - 2 * delta, Img2.get_height() - 2 * delta)
    return first.colliderect(second)


def check_game_state():
    for pipe in pipe_list:
        if isCollision(pipe[1], pipe[2], pipe[0],
                       bird_x, bird_y, bird_img):
            sound_hit.play()
            return False

    if bird_y + bird_img.get_height() - 20 >= base_y or \
       bird_y < -20:
        sound_die.play()
        return False

    return True



def update_score():
    global pipe_list, score, high_score
    for pipe in pipe_list:
        if not pipe[3] and pipe[1] < bird_x and pipe[2] < bird_y:
            sound_point.play()
            score += 1
            pipe[3] = True

        if not pipe[3] and pipe[1] < bird_x:
            pipe[3] = True

    if score > high_score:
        high_score = score



def create_pipe():
    x1 = display_size[0]
    y1 = random.randrange(100, display_size[1] * 3 // 5 - base.get_height())

    pipe_list.append([pygame.transform.scale(pipe_img, (pipe_img.get_width(), y1)),
                      x1, display_size[1] - base.get_height() - y1, False])

    pipe_list.append([pygame.transform.scale(pipe_img_reverse,
                                             (pipe_img_reverse.get_width(),
                                              display_size[1] - (y1 + base.get_height()) - pipe_dist)),
                      x1, 0, False])


def update_pipe():
    for i in range(len(pipe_list)):
        pipe_list[i][1] += pipe_speed

    for pipe in pipe_list:
        if pipe[1] + pipe_img.get_width() <= 0:
            pipe_list.remove(pipe)


def draw_display():
    display.blit(background, (background_x, 0))
    display.blit(background, (background_x + background.get_width(), 0))

    display.blit(bird_img, (bird_x, bird_y))

    for pipe in pipe_list:
        display.blit(pipe[0], (pipe[1], pipe[2]))

    display.blit(base, (base_x, base_y))
    display.blit(base, (base_x + base.get_width(), base_y))


def update_background():
    global background_x
    background_x += background_speed

    if background_x + background.get_width() <= 0:
        background_x = 0


def update_base():
    global base_x
    base_x += base_speed

    if base_x + base.get_width() <= 0:
        base_x = 0


def update_bird():
    global bird_img, bird_move_y, bird_y, game
    bird_img = bird_animation[bird_ind]
    bird_move_y += gravity
    bird_y += bird_move_y
    bird_img = pygame.transform.rotate(bird_img, -bird_move_y * 3)




def UPDATE():
    update_base()
    update_background()
    update_pipe()
    update_bird()


def restart():
    global game, score, bird_x, bird_y, bird_ind, bird_move_y
    global pipe_list

    game = True
    score = 0
    bird_x = 50
    bird_y = display_size[1] / 2 - bird_img.get_height() / 2
    bird_move_y = 0

    pipe_list.clear()

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

        if game:
            if event.type == BIRDFLAP:
                bird_ind = (bird_ind + 1) % len(bird_animation)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    sound_wing.play()
                    bird_move_y = jump

            if event.type == SPAWNPIPE:
                if score % 10 == 0 and score > 0:
                    base_speed -= 0.5
                    pipe_speed = base_speed
                    spawn_speed -= 50
                    pygame.time.set_timer(SPAWNPIPE, spawn_speed)


                create_pipe()


        if event.type == pygame.KEYDOWN and not game and not end:
            if event.key == pygame.K_SPACE:
                restart()

    if game:
        UPDATE()
        draw_display()
        game = check_game_state()
        update_score()


    if not game:
        pass

    score_display()

    pygame.display.update()