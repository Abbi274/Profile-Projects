import pygame 
import os
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()  

FPS = 60 # import and init, frame rate

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
FIXED_KITCHEN = pygame.image.load('fixed_kitchen.png')
FRIDGE = pygame.image.load('fridge.png')
HOOD = pygame.image.load('hood2.png')
OVEN = pygame.image.load('oven2.png')
MIXER = pygame.image.load('mixer.png')
TABLE = pygame.image.load('table.png')
MICROWAVE = pygame.image.load('microwave.png')
CABINETS = pygame.image.load('cabinets.png')
CHAIR = pygame.image.load('yellow_chair.png')
CHAIR2 = pygame.image.load('blue_chair.png')
DERP = pygame.image.load('derp.png')
PICTURE = pygame.image.load('picture.png')
# store each sprite and properties in its own class 
pos_directions = ['u','r','d','l'] # to track pos as rotate  
class Sprite: 
    def __init__(self, name = '', sprite = None, coord = (0,0), final_coord = (0,0), final_angle = 0, pos = 0): 
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
        self.pos = pos # track pos for rotation and locking 
     
    def rotate(self, center_pos): 
        # Rotate the image
        self.image = pygame.transform.rotate(self.orig_image, self.angle) 
        self.rect = self.image.get_rect(center = (center_pos))
        
    def __str__(self): 
        return f'{self.name}'
    
# load in desired angles and desired coords for locking into place
sprite_map = {'cabinets': (CABINETS,(0*cell_h,0*cell_w),(3*cell_w, 5*cell_h), 180,2), 'fridge': (FRIDGE,(1*cell_w,4*cell_h),(12*cell_w, 0),0,0), 'oven':(OVEN,(5*cell_w,10*cell_h),(0, 5*cell_h), 180, 2),  'hood':(HOOD, (6*cell_w,7*cell_h),(-1*cell_w, -1*cell_h), 180,2), 'microwave': (MICROWAVE, (12*cell_w,2*cell_h),(9*cell_w, 4*cell_h), 90, 3), 'chair': (CHAIR, (9*cell_w,5*cell_h),(1*cell_w,7*cell_h),0,0), 'chair2': (CHAIR2, (9*cell_w,9*cell_h),(5*cell_w, 7*cell_h), 0, 0), 'table':(TABLE, (11*cell_w,8*cell_h),(2*cell_w,9*cell_h), 90, 3), 'mixer':(MIXER, (9*cell_h,4*cell_w),(4*cell_w, 3*cell_h), 0,0), 'derp':(DERP,(2*cell_w, 2*cell_h),(11*cell_w,10*cell_h),0,0), 'picture': (PICTURE, (0, 2*cell_h), (5*cell_w, 0), 0, 0)}

sprite_classes = [Sprite(name, val[0], val[1], val[2], val[3], val[4]) for name, val in sprite_map.items()]

# load init images 
WINDOW_SURFACE.blit(EMPTY_KITCHEN,(0,0))
for sprite in sprite_classes:  
    WINDOW_SURFACE.blit(sprite.image, sprite.rect)

# redefine angle of rotation within the sprite 
def rotate_sprite(key, sprite): # already confirmed key is either l or r arrow 
    center_pos = sprite.rect.center 
    new_angle = 0 
    new_pos = 0
    if key == pygame.K_RIGHT: 
        new_angle = sprite.angle + 90 # turn by 90 % 
        # and turn each object pos based on turn 
        new_pos = (sprite.pos + 1) % 4
    if key == pygame.K_LEFT: 
        new_angle = sprite.angle - 90 
        new_pos = (sprite.pos - 1) % 4
    
    # set the new angle 
    sprite.angle = new_angle % 360
    sprite.rotate(center_pos) # rotate the orig image by new angle and set the rect pos
    sprite.pos = new_pos 
    
def main(): 

    clock = pygame.time.Clock() # run the game at set fps 

    dragging = False 
    dragging_item = None 
    dragging_rect = None 
    last_rect = None
    all_locked = 0 
    last_object = None 
    run = True 
    background = EMPTY_KITCHEN
    set_sprites = False 

    while run: 

        clock.tick(FPS) # run the game at set fps 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # if quit or esp key 
                run = False    # force exit 

            if event.type == pygame.MOUSEBUTTONDOWN: 
                # what happens when click down on the mouse 
                # get mouse pos and if interactible rect then dragging and grab
                mouse_pos = event.pos 
                for sprite in sprite_classes:
                    if sprite.rect.collidepoint(mouse_pos): 
                        dragging = True 
                        dragging_item = sprite
                           
            # drag the item 
            if event.type == pygame.MOUSEMOTION and dragging and dragging_item.can_move: 
                dragging_item.rect.center = event.pos

            # stop dragging item if mouseup 
            if event.type == pygame.MOUSEBUTTONUP:
                # store last clicked to rotate 
                last_object = dragging_item 
                dragging = False 
                dragging_item = None  

                # check if we can 'lock' this item into place 
                # give area 15 by 15 pixel grace to desired final pos 
                x,y = last_object.rect.topleft[0], last_object.rect.topleft[1] 
                # get the difference of the final x and y where placed - the desired x and y and see if in desireable range  
        
                if abs(x - last_object.final_coord[0]) <= 30 and abs(y - last_object.final_coord[1]) <= 30:
                    # give 15 degree grace area to the desired final angle 
                    if abs(last_object.angle - last_object.final_angle) <= 30: 
                        if pos_directions[last_object.pos] == 'u' and last_object.can_move:  
                            print(f'{last_object} locked!')
                            last_object.can_move = False 
                            last_object = None 
                            all_locked += 1 
                
            if event.type == pygame.KEYDOWN and last_object: 
                key_pressed = event.key
                if key_pressed in [pygame.K_LEFT, pygame.K_RIGHT]: 
                    rotate_sprite(key_pressed, last_object) 

            if all_locked == 11:
                set_sprites = True  
                WINDOW_SURFACE.fill(WHITE)
                background = FIXED_KITCHEN
            
            WINDOW_SURFACE.blit(background,(0,0))
            if set_sprites == False: 
                for sprite in sprite_classes:  
                    WINDOW_SURFACE.blit(sprite.image, sprite.rect)
            pygame.display.update()

          

    # force quit and exit when user stops run or code stops run 
    pygame.quit()
    sys.exit()

    
if __name__ == "__main__": # run the main code if in the main script 

    main()