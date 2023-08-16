import pygame,os,sys
import random
from time import sleep, time
pygame.init()
from assets.scripts.Tleng2 import *

FPS = 60
CLOCK = pygame.time.Clock()

WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Give Me All The Coins - RainCoin")

VEL = 8

POLICE_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets','art','police.wav'))

COIN_BACKPACK_SOUND = pygame.mixer.Sound(os.path.join('assets','art','coin-backpack.wav'))
COIN_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets','art','coin-ground.wav'))

Background = Entity(WIN,0,0,WIDTH,HEIGHT,'Background',img_filename=os.path.join('assets','art','Bank.png'))

coins = []
for i in range(5):
    coins += [Entity(WIN, 0, 0, 40, 40, 'enemy', img_filename=os.path.join('assets','art','coin.png'))]
for coin in coins:
    randx, randy = random.randint(40,460),-(random.randint(100,500))
    coin.rect.x = randx
    coin.imageX = randx
    coin.rect.y = randy
    coin.imageY = randy

backpack = Entity(WIN, 0, 500, 70, 70, 'player', img_filename=os.path.join('assets','art','backpack.png'))

score = Label(WIN, 10,10,100,10)
score.set_Label(0)

COIN_HIT = pygame.USEREVENT + 1

def backpack_handle_movement(keys_pressed, backpack):
    if keys_pressed[pygame.K_a] and backpack.rect.x - VEL > 0: # left
        backpack.rect.x -= VEL
        backpack.imageX -= VEL
    if keys_pressed[pygame.K_d] and backpack.rect.x + VEL + backpack.coreWidth < WIDTH: # right
        backpack.rect.x += VEL
        backpack.imageX += VEL

def coin_dropping(coins,time1):
    for coin in coins:
        if colliderect(coin.rect, backpack.rect):
            score.score += 1
            COIN_BACKPACK_SOUND.play()
            randx, randy = random.randint(40,460),-(random.randint(100,500))
            coin.rect.x = randx
            coin.imageX = randx
            coin.rect.y = randy
            coin.imageY = randy
        if coin.rect.y + VEL + coin.coreHeight < HEIGHT and coin.imageY + VEL + coin.coreHeight < HEIGHT: # right
            vel = VEL*(time()-time1)/20
            coin.rect.y += vel
            coin.imageY += vel
        if collidepoint(coin.rect,coin.rect.x,HEIGHT-coin.rect.height):
            coins.remove(coin)
            COIN_HIT_SOUND.play()
            if len(coins) < 2:
                POLICE_HIT_SOUND.play()
                sleep(1)
                return "lost"


def draw_window(current_fps,time1):
    #displaying the bacground image
    Background.display_idle(0,0)
    backpack.display_current_anim(FPS,current_fps)

    gamestate = coin_dropping(coins, time1)
    if gamestate == 'lost':
        return 'lost'

    backpack.display_current_anim(FPS,current_fps)
    backpack.outline_Area(5,RED)
    score.draw_Label(100,5)

    for i in coins:
        i.display_current_anim(FPS,current_fps)
        i.outline_Area(5,RED)

    pygame.display.update()

def main():
    run = True
    time1 = time()
    while run:
        CLOCK.tick(FPS)
        current_fps = CLOCK.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        backpack_handle_movement(keys_pressed,backpack)
        if draw_window(current_fps,time1) == "lost":

            run = False
            pygame.quit()
            sys.exit()            

if __name__ == "__main__":
    main()