# my stupid attempt at a Snake game.

import pygame, random
from collections import deque
from pygame.locals import *

BLACK = (0, 0, 0)
AMBER = (255, 128, 0)

PLAY_WIDTH = 40
PLAY_HEIGHT = 40

CHAR_WIDTH = 9
CHAR_HEIGHT = 18
HALF_CHAR_HEIGHT = CHAR_HEIGHT//2

SCREEN_WIDTH = CHAR_WIDTH*80
SCREEN_HEIGHT = CHAR_HEIGHT*25
CENTER_HEIGHT = SCREEN_HEIGHT//2

BOX_LEFT_OUT = 4*CHAR_WIDTH
BOX_LEFT_IN = 5*CHAR_WIDTH
BOX_RIGHT_IN = BOX_LEFT_IN + PLAY_WIDTH*CHAR_WIDTH
BOX_RIGHT_OUT = BOX_RIGHT_IN + CHAR_WIDTH
BOX_TOP_IN = CENTER_HEIGHT - HALF_CHAR_HEIGHT*PLAY_HEIGHT//2
BOX_TOP_OUT = BOX_TOP_IN - HALF_CHAR_HEIGHT
BOX_BOTTOM_IN = CENTER_HEIGHT + HALF_CHAR_HEIGHT*PLAY_HEIGHT//2
BOX_BOTTOM_OUT = BOX_BOTTOM_IN + HALF_CHAR_HEIGHT
BOX_HEIGHT = PLAY_HEIGHT*HALF_CHAR_HEIGHT
BOX_HEIGHT_OUT = BOX_HEIGHT + CHAR_HEIGHT
BOX_WIDTH = PLAY_WIDTH*CHAR_WIDTH
BOX_WIDTH_OUT = BOX_WIDTH + 2*CHAR_WIDTH

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.init()
screen = pygame.display.set_mode(size)

pygame.display.set_caption("SNAKE")

grow = 0
state = 0

snake = deque()

crash = 0
flash = 0
score = 0
score_tick = 0;

def dsquared(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def draw_screen():
    global flash, crash, score
    if state == 2:
        if crash < 10:
            crash += 1
        flash = crash%2

    if flash:
        pygame.draw.rect(screen, AMBER, (BOX_LEFT_OUT, BOX_TOP_OUT,
                                         BOX_WIDTH_OUT, BOX_HEIGHT_OUT))
    else:
        # upper border
        pygame.draw.rect(screen, AMBER, (BOX_LEFT_OUT, BOX_TOP_OUT,
                                         BOX_WIDTH_OUT, HALF_CHAR_HEIGHT))
        # bottom border
        pygame.draw.rect(screen, AMBER, (BOX_LEFT_OUT, BOX_BOTTOM_IN,
                                         BOX_WIDTH_OUT, HALF_CHAR_HEIGHT))
        # left border
        pygame.draw.rect(screen, AMBER, (BOX_LEFT_OUT, BOX_TOP_IN,
                                         CHAR_WIDTH, BOX_HEIGHT)) 
        # right border
        pygame.draw.rect(screen, AMBER, (BOX_RIGHT_IN, BOX_TOP_IN,
                                         CHAR_WIDTH, BOX_HEIGHT))
    # draw snake
    if flash:
        color = BLACK
    else:
        color = AMBER
    for i in snake:
        pygame.draw.rect(screen, color,
                         (BOX_LEFT_IN + CHAR_WIDTH*i[0],
                          BOX_TOP_IN + HALF_CHAR_HEIGHT*i[1],
                          CHAR_WIDTH, HALF_CHAR_HEIGHT))
    if egg_flag: # draw egg
        # top
        pygame.draw.rect(screen, color,
                         (CHAR_WIDTH*egg[0] - CHAR_WIDTH + BOX_LEFT_IN,
                          HALF_CHAR_HEIGHT*egg[1] - HALF_CHAR_HEIGHT + BOX_TOP_IN,
                          3*CHAR_WIDTH, HALF_CHAR_HEIGHT))
        # bottom
        pygame.draw.rect(screen, color,
                         (CHAR_WIDTH*egg[0] - CHAR_WIDTH + BOX_LEFT_IN,
                          HALF_CHAR_HEIGHT*egg[1] + HALF_CHAR_HEIGHT + BOX_TOP_IN,
                          3*CHAR_WIDTH, HALF_CHAR_HEIGHT))
        # left
        pygame.draw.rect(screen, color,
                         (CHAR_WIDTH*egg[0] - CHAR_WIDTH + BOX_LEFT_IN,
                          HALF_CHAR_HEIGHT*egg[1] + BOX_TOP_IN,
                          CHAR_WIDTH, HALF_CHAR_HEIGHT))
        # right
        pygame.draw.rect(screen, color,
                         (CHAR_WIDTH*egg[0] + CHAR_WIDTH + BOX_LEFT_IN,
                          HALF_CHAR_HEIGHT*egg[1] + BOX_TOP_IN,
                          CHAR_WIDTH, HALF_CHAR_HEIGHT))
    font = pygame.font.SysFont('Calibri', CHAR_HEIGHT)
    text = font.render("S N A K E", False, AMBER)
    screen.blit(text, [BOX_RIGHT_OUT+100, 100])
    if score == 0:
        text= font.render("Score: 0", False, AMBER)
    else:
        text = font.render("Score: " + str(score) + "0", False, AMBER)
    screen.blit(text, [BOX_RIGHT_OUT+100, 150])
    if state == 2:
        text = font.render("Play again? (y/n)", False, AMBER);
        screen.blit(text, [BOX_RIGHT_OUT+100, 200])
        
def game_update():
    global grow, state, direction
    global egg, egg_flag, egg_clock
    global crash, score, score_tick
    if state == 0: # start a new game
        snake.clear()
        snake.append((20,20))
        direction = RIGHT;
        state = 1
        grow = 5
        crash = 0
        score = 0
        score_tick = 10;
        egg_clock = 20
        egg_flag = False
    elif state == 1: # in game
        score_tick -= 1
        if score_tick < 0:
            score_tick = 10
            if score > 0:
                score -= 1
        head = snake[-1]
        if direction == DOWN:
            new_head = (head[0], head[1]+1)
        elif direction == UP:
            new_head = (head[0], head[1]-1)
        elif direction == LEFT:
            new_head = (head[0]-1, head[1])
        else:
            new_head = (head[0]+1, head[1])
        if new_head[0] < 0 or new_head[0] >= PLAY_WIDTH \
            or new_head[1] < 0 or new_head[1] >= PLAY_HEIGHT:  
            state = 2
        elif new_head in snake:
            state = 2
        else:
            snake.append(new_head)
            if grow > 0:
                grow -= 1
            else:
                snake.popleft()
            if egg_flag:
                if dsquared(new_head, egg) < 3:
                    egg_flag = False
                    egg_clock = 21
                    grow = 5
                    score += len(snake) - 1
            
            egg_clock -= 1
            if egg_clock == 0:
                if egg_flag:
                    egg_flag = False
                    egg_clock = 20
                else:
                    egg = (random.randrange(38)+1, random.randrange(38)+1)
                    for e in snake:
                        if dsquared(e, egg) < 3:
                            egg_clock = 1
                            break;
                    else:
                        egg_flag = True
                        egg_clock = 20


def game_key(k):
    global state, direction, done
    if state == 1:
        if k == K_UP or k == K_KP8:
            direction = UP
        elif k == K_DOWN or k == K_KP2:
            direction = DOWN
        elif k == K_LEFT or k == K_KP4:
            direction = LEFT
        elif k == K_RIGHT or k == K_KP6:
            direction = RIGHT                
    elif state == 2:
        if k == K_y:
            state = 0
        elif k == K_n:
            done = True
            
done = False
pygame.time.set_timer(USEREVENT, 100)
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            game_key(event.key)
        elif event.type == USEREVENT:
            screen.fill(BLACK)
            game_update()
            draw_screen()
            pygame.display.flip()

pygame.quit()

