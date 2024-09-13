import pygame 
import os
import sys
import asyncio
import pygbag 

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets\Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60 
MAX_BULLETS = 5
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40 
VEL = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE_BACKGROUND,(0,0))  
    
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10 ))
    WIN.blit(red_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    
    for bullet in red_bullets: 
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets: 
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def red_handle_movement(keys_pressed, red): 
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: #left 
        red.x -= VEL
    if keys_pressed[pygame.K_d]and red.x + VEL < WIDTH//2 - 40: #right 
        red.x += VEL
    if keys_pressed[pygame.K_w]and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_s]and red.y + VEL < 450: #down 
        red.y += VEL


def yellow_handle_movement(keys_pressed, yellow): 
    if keys_pressed[pygame.K_LEFT] and yellow.x + VEL > WIDTH//2 + 10: #left 
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT]and yellow.x - VEL < 850: #right 
        yellow.x += VEL
    if keys_pressed[pygame.K_UP]and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN]and yellow.y + VEL < 450: #down 
        yellow.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets: 
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets: 
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) 
            red_bullets.remove(bullet) 
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

async def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_width()//2 + 100))
    pygame.display.update()
    await asyncio.sleep(5) #5 seconds

async def main():
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # x,y  
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    clock = pygame.time.Clock()

    red_bullets =[]
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    while run: 
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False 
                # no need to explicity quit - handled by the browser 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS: 
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) 
                    red_bullets.append(bullet) 
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1 
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''

        if red_health <= 0:
            await asyncio.sleep(10) 
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            await asyncio.sleep(10)
            winner_text = "Red Wins!"
        
        if winner_text != '':
            await draw_winner(winner_text)
            break

        await asyncio.sleep(1/FPS)
        # if you want user to be able to press multiple keys at once
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()





if __name__ == "__main__": 
    asyncio.run(main())