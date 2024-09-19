import pygame 
import os
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

'''WIDTH,HEIGHT = 900,500
WINDOW_SURFACE = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Grid")
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
WINDOW_SURFACE.fill(WHITE)
  
n = 15 
m = 15 
cell_w, cell_h = WIDTH/m, HEIGHT/n

EMPTY_KITCHEN = pygame.image.load('empty kitchen.png')
FRIDGE = pygame.image.load('fridge.png')
HOOD = pygame.image.load('hood.png')
OVEN = pygame.image.load('oven2.png')
MIXER = pygame.image.load('mixer.png')
TABLE = pygame.image.load('table.png')
MICROWAVE = pygame.image.load('microwave.png')
CABINETS = pygame.image.load('cabinets.png')
CHAIR = pygame.image.load('chair.png')
CHAIR2 = pygame.image.load('chair2.png')
DERP = pygame.image.load('derp.png')
FIXED_KITCHEN = pygame.image.load('fixed_kitchen.png')'''

# set display, size, cell size, sprite w/h
m = 15 
n = 15 
WIDTH, HEIGHT = 900,500
WINDOW_SURFACE = pygame.display.set_mode((WIDTH,HEIGHT)) 
cell_w, cell_h = WIDTH//m, HEIGHT//n

# colors 
WHITE = (255,255,255) 
BLACK = (0,0,0)

# load music, backgrounds, sprites
EMPTY_KITCHEN = pygame.image.load('empty kitchen.png')
FRIDGE = pygame.image.load('fridge.png')
HOOD = pygame.image.load('hood2.png')
OVEN = pygame.image.load('oven2.png')
MIXER = pygame.image.load('mixer.png')
TABLE = pygame.image.load('table.png')
MICROWAVE = pygame.image.load('microwave.png')
CABINETS = pygame.image.load('cabinets.png')
CHAIR = pygame.image.load('chair.png')
CHAIR2 = pygame.image.load('chair2.png')
DERP = pygame.image.load('derp.png')
FIXED_KITCHEN = pygame.image.load('fixed_kitchen.png')
EMPTY_KITCHEN2 = pygame.image.load('empty kitchen2.png')
# store each sprite and properties in its own class 

class Sprite: 
    def __init__(self, name = '', sprite = None, coord = (0,0), final_coord = (0,0), final_angle = 0): 
        self.coord = coord 
        self.orig_image = sprite # to revert back to orignal pos 
        self.orig_rect = self.orig_image.get_rect(topleft = self.coord)
        self.final_coord = final_coord
        self.can_move = True

        self.name = name
        self.image = sprite
        self.rect = self.image.get_rect(topleft = self.coord) 
        self.angle = 0  
        self.final_angle = final_angle

    def rotate(self, center_pos): 
        # Rotate the image
        self.image = pygame.transform.rotate(self.orig_image, self.angle) 
        self.rect = self.image.get_rect(center = (center_pos))
        
    def __str__(self): 
        return f'{self.name}'
    
# load in desired angles and desired coords for locking into place
sprite_map = {'cabinets': (CABINETS,(0*cell_h,0*cell_w),(3*cell_w, 5*cell_h)), 'fridge': (FRIDGE,(1*cell_w,4*cell_h),(12*cell_w, 0)), 'oven':(OVEN,(3*cell_w,10*cell_h),(0, 4*cell_h)), 'mixer':(MIXER, (9*cell_h,4*cell_w),(4*cell_w, 3*cell_h)), 'hood':(HOOD, (6*cell_w,7*cell_h),(6*cell_w, 0)), 'microwave': (MICROWAVE, (12*cell_w,2*cell_h),(9*cell_w, 3*cell_h)), 'chair': (CHAIR, (9*cell_w,5*cell_h),(2*cell_w,8*cell_h)), 'chair2': (CHAIR2, (8*cell_w,8*cell_h),(5*cell_w, 8*cell_h)), 'table':(TABLE, (11*cell_w,8*cell_h),(2*cell_w,9*cell_h)), 'derp':(DERP,(2*cell_w, 2*cell_h),(11*cell_w,10*cell_h))}
sprite_classes = [Sprite(name, val[0], val[1], val[2]) for name, val in sprite_map.items()] 
 

def draw_grid(surface, grid_color= BLACK, line_width=1):

    for column in range(n + 1):
        x = column * cell_w
        pygame.draw.line(surface, grid_color, (x, 0), (x, HEIGHT), line_width)

    for row in range(m + 1):
        y = row * cell_h
        pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y), line_width)
    pygame.display.update()

draw_grid(WINDOW_SURFACE, BLACK, 1)
WINDOW_SURFACE.blit(EMPTY_KITCHEN2,(0,0))
WINDOW_SURFACE.blit(CHAIR2, (5*cell_w, 7*cell_h))

'''for r in range(m): 
    for c in range(n):
        x, y = c*cell_w, r*cell_h 
        if r == 3 and c == 1: 
            WINDOW_SURFACE.blit(FRIDGE,(x,y))
        elif r == 3 and c == 2: 
            WINDOW_SURFACE.blit(OVEN,(x,y)) 
        elif r == 3 and c == 3:      
            WINDOW_SURFACE.blit(TABLE,(x,y))'''

# redefine angle of rotation within the sprite 
def rotate_sprite(key, sprite): 
    center_pos = sprite.rect.center  
    if key == pygame.K_RIGHT: 
        sprite.angle += 15  
    elif key == pygame.K_LEFT: 
        sprite.angle -= 15 
    sprite.rotate(center_pos)

FPS = 60 


def main():

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS) # run the game at set fps 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        start_button_rect = pygame.Rect(cell_w*5,cell_h*11, cell_w*6,cell_h*5)
        start_button_surface = pygame.Surface((start_button_rect.width, start_button_rect.height))
        table_rect = pygame.Rect(cell_w*4,cell_h*6, cell_w*9,cell_h*5)
        table_surface = pygame.Surface((table_rect.width, table_rect.height))
        table_surface.fill(BLACK)    
        WINDOW_SURFACE.blit(start_button_surface, start_button_rect.topleft)
        pygame.display.update()

    pygame.quit()

    sys.exit()


if __name__ == "__main__":
    main()