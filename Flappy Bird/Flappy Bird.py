import pygame
import time 
import random
import os

from pygame import mixer

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

FPS = 60

#   Colors
black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

#   Display
display_width = 1000
display_height = 850
gameDisplay = pygame.display.set_mode((display_width, display_height))
# gameDisplay is our Surface
pygame.display.set_caption('Flappy Bird')
game_icon = pygame.image.load('Assets/Sprites/Other/game_icon.png')
pygame.display.set_icon(game_icon)

clock = pygame.time.Clock()

class Flappy_Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__(self)
        self.x = display_width / 5
        self.y = display_height / 2
        self.score = 0

        self.dx = 0
        self.dy = 5

        self.angle = 0.00

        self.bird_image = pygame.image.load('Assets/Sprites/Flappy Bird/Flappy_Bird.png').convert_alpha()
        self.w, self.h = self.bird_image.get_size()
        self.bird_image = pygame.transform.scale(self.bird_image, (self.w + 25, self.h + 25))
        self.w, self.h = self.bird_image.get_size()
        # self.rect = self.bird_image.get_rect()
    

    def blitRotate(self, pos, angle):

        originPos = (self.w / 2, self.h / 2)

        # calcaulate the axis aligned bounding box of the rotated image
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (self.w, 0), (self.w, -self.h), (0, -self.h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(self.bird_image, angle)

        # rotate and blit the image
        gameDisplay.blit(rotated_image, origin)

pipe_speed = -3
class Obstacles(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__(self)
        self.H = 165
        self.x = display_width
        self.y = random.randrange(self.H, display_height - self.H)

        self.dx = pipe_speed
        self.dy = 0
        # self.dH = -25
        # self.H_min = 150

        self.vis = False

        self.obs_image1 = pygame.image.load('Assets/Sprites/Obstacles/Flappy_Bird_Pipe1.png').convert_alpha()
        self.w1, self.h1 = self.obs_image1.get_size()
        self.obs_image1 = pygame.transform.scale(self.obs_image1, (self.w1 + 100, self.h1 + 500))
        self.w1, self.h1 = self.obs_image1.get_size()

        self.obs_image2 = pygame.image.load('Assets/Sprites/Obstacles/Flappy_Bird_Pipe2.png').convert_alpha()
        self.w2, self.h2 = self.obs_image2.get_size()
        self.obs_image2 = pygame.transform.scale(self.obs_image2, (self.w2 + 100, self.h2 + 500))
        self.w2, self.h2 = self.obs_image2.get_size()
        # self.rect = self.obs_image1.get_rect()


    def obs(self, x, y):
        gameDisplay.blit(self.obs_image1, (x,y + self.H))
        gameDisplay.blit(self.obs_image2, (x,y - self.h2 - self.H))

    def update(self):
        if self.x < display_width / 2:
            del self

class coin(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.coin_image = pygame.image.load('Assets/Sprites/Coins/Flappy_Bird_Coin.png').convert_alpha()
        self.w, self.h = self.coin_image.get_size()
        self.coin_image = pygame.transform.scale(self.coin_image, (self.w - 290, self.h - 350))
        self.w, self.h = self.coin_image.get_size()

        self.x = random.randrange(display_width, display_width + self.w + 1)
        self.y = random.randrange(self.h, display_height - self.h + 1)

        self.dx = pipe_speed
        self.dy = 0

    def coinxy(self):
       gameDisplay.blit(self.coin_image, (self.x, self.y))

    def check(self, x, y):
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        return False
    
    def update(self):
        self.x += self.dx


#  to display msg
def create_font(text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    msg = font.render(text, True, color)
    gameDisplay.blit(msg, (x, y))


def crash(score):
    mixer.music.stop()
    # gameover_sound = pygame.mixer.Sound("gameover.wav")
    # gameover_sound.play()
    bird_die_sound = pygame.mixer.Sound("Assets/Sounds/bird_die.wav")
    bird_die_sound.play()
    create_font('You Died', 70, black, display_width / 3, 5*display_height / 12)
    create_font('Your Score : ' + str(score), 70, black, display_width / 3 - 50, 5*display_height / 12 + 85)
    pygame.display.update()
    time.sleep(4)
    game_over()
    pygame.quit()
    quit()

def Scoreboard(score):
    create_font("Scoreboard : " + str(score), 50, black, 0, 0)

def boundary(b, x, y, score):
    if x - b.w / 2 < 0:
        x = b.w / 2
    if x + b.w / 2 > display_width:
        x = display_width - b.w / 2
    if y - b.h / 2 < 0:
        y = b.h / 2
    if y - b.h / 2 > display_height:
        # y = display_height - b.h / 2
        crash(score)
    return (x, y)


class Button:

    def __init__(self, msg, font_size, x, y, w, h):
        self.msg = msg
        self.font_size = font_size
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw_button(self, color):
        pygame.draw.rect(gameDisplay, color, [self.x, self.y, self.w, self.h])
        # create_font(text, size, color, x, y)
        create_font(self.msg, self.font_size, black, self.x + 3*self.w / 16, self.y + self.h / 4)

gameover_sound = pygame.mixer.Sound("Assets/Sounds/gameover.wav")
def game_over():

    over = True

    game_over = pygame.image.load('Assets/Backgrounds/game_over.jpg')
    w, h = game_over.get_size()
    game_over = pygame.transform.scale(game_over, (w + 165, h + 380))

    # Button(msg, font_size, x, y, w, h)
    restart_button = Button('Restart', 32, 100, 650, 165, 60)
    exit_button = Button('Exit', 32, 800, 650, 100, 60)

    gameover_sound.play()

    while over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(game_over, (0, 0))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if restart_button.x < mouse[0] < restart_button.x + restart_button.w and restart_button.y < mouse[1] < restart_button.y + restart_button.h:
            restart_button.draw_button(bright_green)
            if click[0]:
                gameover_sound.stop()
                game_intro()
        else:
            restart_button.draw_button(green)

        if exit_button.x < mouse[0] < exit_button.x + exit_button.w and exit_button.y < mouse[1] < exit_button.y + exit_button.h:
            exit_button.draw_button(bright_red)
            if click[0]:
                pygame.quit()
                quit()
        else:
            exit_button.draw_button(red)

        pygame.display.update()


def pause_menu():

    pause = True

    pause_image = pygame.image.load('Assets/Backgrounds/game_pause.jpg')
    w, h = pause_image.get_size()
    pause_image = pygame.transform.scale(pause_image, (w, h + 100))

    # self, msg, font_size, x, y, w, h
    continue_button = Button('Continue', 32, 150, 550, 200, 60)
    exit_button = Button('Exit', 32, 750, 550, 100, 60)

    while pause:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(pause_image, (0, 0))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if continue_button.x < mouse[0] < continue_button.x + continue_button.w and continue_button.y < mouse[1] < continue_button.y + continue_button.h:
            continue_button.draw_button(bright_green)
            if click[0]:
                pause = False
        else:
            continue_button.draw_button(green)

        if exit_button.x < mouse[0] < exit_button.x + exit_button.w and exit_button.y < mouse[1] < exit_button.y + exit_button.h:
            exit_button.draw_button(bright_red)
            if click[0]:
                pygame.quit()
                quit()
        else:
            exit_button.draw_button(red)

        pygame.display.update()    

intro_sound = pygame.mixer.Sound("Assets/Sounds/intro_sound.wav")
def game_intro():
    
    gameover_sound.stop()
    intro = True
    
    intro_image = pygame.image.load('Assets/Backgrounds/game_intro.png').convert_alpha()
    w, h = intro_image.get_size()
    intro_image = pygame.transform.scale(intro_image, (w + 490, h + 400))
    
    # Button(msg, font_size, x, y, w, h)
    play_button = Button('Play !', 32, 100, 650, 125, 60)
    credit_button = Button('Credits', 32, 450, 650, 165, 60)
    exit_button = Button('Exit', 32, 800, 650, 100, 60)

    intro_sound.play()

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(intro_image, (0, 0))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        create_font('Flappy Bird', 110, black, 215, 35)
        
        if play_button.x < mouse[0] < play_button.x + play_button.w and play_button.y < mouse[1] < play_button.y + play_button.h:
            play_button.draw_button(bright_green)
            if click[0]:
                intro_sound.stop()
                game_loop()
        else:
            play_button.draw_button(green)
        if credit_button.x < mouse[0] < credit_button.x + credit_button.w and credit_button.y < mouse[1] < credit_button.y + credit_button.h:
            credit_button.draw_button(bright_blue)
            if click[0]:
                game_credit()
        else:
            credit_button.draw_button(blue)
        if exit_button.x < mouse[0] < exit_button.x + exit_button.w and exit_button.y < mouse[1] < exit_button.y + exit_button.h:
            exit_button.draw_button(bright_red)
            if click[0]:
                pygame.quit()
                quit()
        else:
            exit_button.draw_button(red)

        pygame.display.update()


def game_credit():

    credit = True

    return_button = Button('Return', 32, 400, 680, 165, 60)
    insta_logo = pygame.image.load('Assets/Sprites/Other/instagram_logo.png')
    w, h = insta_logo.get_size()
    insta_logo = pygame.transform.scale(insta_logo, (w - 1380, h - 1390))

    while credit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        gameDisplay.fill(black)
        # create_font(text, size, color, x, y)
        create_font('##UniTy', 65, white, 745, 5)
        create_font('Credits :', 50, white, 400, 175)
        create_font('Game Development                  : Akshat', 40, white, 63, 300)
        create_font('Assets Editing and Guidance : Abhishek Verma', 40, white, 63, 350)
        create_font(' Follow Us On Instagram         - ', 40, white, 75, 500)
        create_font(' @no_surname_', 40, white, 75, 550)
        create_font(' @abhishek_didot', 40, white, 75, 600)

        gameDisplay.blit(insta_logo, (560, 473))

        if return_button.x < mouse[0] < return_button.x + return_button.w and return_button.y < mouse[1] < return_button.y + return_button.h:
            return_button.draw_button(bright_green)
            if click[0]:
                game_intro()
        else:
            return_button.draw_button(green)

        pygame.display.update()


def game_loop():

    gameExit = False
    intro_sound.stop()
    gameover_sound.stop()
    mixer.music.load('Assets/Sounds/Mario-theme-song.wav')
    mixer.music.play(-1)

    score = 0
    
    t_pipe_min = 2500
    t_start_pipe = 4000
    dt = -250
    ADDPIPE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDPIPE, t_start_pipe)

    t_coin_min = 950
    t_start_coin = 1000
    dt_coin = -5
    coin_max = 5
    ADDCOIN = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCOIN, t_start_coin)

    b = []
    b.append(Flappy_Bird())


    o = []
    o.append(Obstacles())

    coins = []
    coins.append(coin())
    coin_sound = pygame.mixer.Sound("Assets/Sounds/coin_sound.wav")

    vis1 = [False]*5000

    bg = pygame.image.load("Assets/Backgrounds/game_background.jpg").convert_alpha()
    f = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == ADDPIPE:
                o.append(Obstacles())
            if event.type == ADDCOIN:
                c = coin()
                # coin_max = random.randrange(1, 6)
                # for i in range(coin_max):
                coins.append(c)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mixer.music.pause()
                    pause_menu()
                    mixer.music.unpause()
                if event.key == pygame.K_LEFT:
                    b[0].dx = -5
                elif event.key == pygame.K_RIGHT:
                    b[0].dx = 4
                if event.key == pygame.K_DOWN:
                    b[0].dy += 5
                elif event.key == pygame.K_UP:
                    b[0].dy = -10
                    f = True
                # if event.key == pygame.K_ESCAPE:
                    # pause_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    b[0].dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    b[0].dy = 10
                    f = False

        # background image
        gameDisplay.blit(bg, (0, 0))
        # gameDisplay.fill(white)

        for c in coins:
            for p in o:
                if p.x < c.x < p.x + p.w1 or p.x < c.x + c.w < p.x + p.w1:
                    if c.y < p.y - p.H or p.y + p.H < c.y + c.h:
                        coins.remove(c)

        # for c1 in coins:
        #     for c2 in coins:
        #         if c1.x < c2.x < c1.x + c1.w and c1.y < c2.y < c1.y + c1.h:
        #             coins.remove(c2)
        
        # for c in coins:
        #     if c.x + c.w < 0:
        #         coins.remove(c)

        #   For Bird's position and angle - blit
        b[0].x += b[0].dx
        b[0].y += b[0].dy

        if f:
            b[0].angle += 0.65
            if b[0].angle > 0:
                b[0].angle = 0
        else:
            b[0].angle -= 0.45
            if b[0].angle < -45:
                b[0].angle = -45
        b[0].blitRotate((b[0].x, b[0].y), b[0].angle)
        (b[0].x, b[0].y) =  boundary(b[0], b[0].x, b[0].y, score)

        for p in o:
            p.x += p.dx
            p.obs(p.x, p.y)
            if p.x + p.w1 < 0:
                o.remove(p)
            if p.x + p.w1 < b[0].x and not p.vis:
                score += 1
                p.vis = True
            
            # restricting from moving inside the pipe from its head and perpendicular to the pipe's length
            if p.x < b[0].x + b[0].w / 2 < p.x + p.w1 or p.x < b[0].x - b[0].w / 2 < p.x + p.w1:
                if b[0].y - b[0].h / 2 < p.y - p.H:
                    # b[0].y = p.y - p.H + b[0].h / 2
                    crash(score)
                if b[0].y + b[0].h / 2 > p.y + p.H:
                    # b[0].y = p.y + p.H - b[0].h / 2
                    crash(score)

        for c in coins:
            c.update()
            c.coinxy()

            if c.check(b[0].x, b[0].y) or c.check(b[0].x + b[0].w, b[0].y) or c.check(b[0].x, b[0].y + b[0].h) or c.check(b[0].x + b[0].w, b[0].y + b[0].h):
                coins.remove(c)
                score += 1
                # pygame.mixer.stop()
                # coin_sound.play()

        if score % 5 == 0 and not vis1[score]:
            t_start_pipe += dt
            vis1[score] = True
            # print(t_start_pipe)
            if t_start_pipe < t_pipe_min:
                t_start_pipe = t_pipe_min
            pygame.time.set_timer(ADDPIPE, t_start_pipe)
            t_start_coin += dt_coin
            if t_start_coin < t_coin_min:
                t_start_coin = t_coin_min
            pygame.time.set_timer(ADDCOIN, t_start_coin) 
            
            
        Scoreboard(score)

        pygame.display.update()
        clock.tick(FPS)

game_intro()
game_loop()
pygame.quit()
quit()