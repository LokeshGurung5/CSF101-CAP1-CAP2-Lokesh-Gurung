import pygame
from pygame.locals import *
import random

pygame.init()

#create the window
game_width = 900
game_height = 500
screen_size = (game_width, game_height)
game_window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Shooting gallery')

#load images
images = {}
def load_image(name, filename, flip_x = False):
    images[name] = pygame.image.load(filename).convert_alpha()

    #flip image on the x-axis
    if flip_x:
        images[name] = pygame.transform.flip(images[name], True, False)

load_image('bg', 'images/bg_blue.png')
load_image('table', 'images/bg_wood.png')
load_image('curtain_top', 'images/curtain_straight.png')
load_image('curtain_left', 'images/curtain.png')
load_image('curtain_right', 'images/curtain.png', True)
load_image('water_back', 'images/water1.png')
load_image('water_front', 'images/water2.png')
load_image('grass', 'images/grass1.png')
load_image('duck_yellow', 'images/duck_outline_yellow.png')
load_image('duck_yellow_target', 'images/duck_outline_target_yellow.png')
load_image('duck_brown','images/duck_outline_brown.png', True)
load_image('duck_brown_target', 'images/duck_outline_target_brown.png', True)
load_image('stick_metal', 'images/stick_metal.png')

class Duck(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        #randomly adjust the y coordinates to vary the heights of the ducks
        self.y += random.randint(0, 5) * 10

        #keep tract of whether this duck has been hit or not
        self.is_hit = False

    def draw(self):

        #draw the duck if it hasn't been hit yet
        if self.is_hit == False:
            game_window.blit(self.image, (self.x, self.y))

        #draw the stick image
        stick_x = self.x + self.image.get_width() / 2 - images['stick_metal'].get_width() / 2
        stick_y = self.y + self.image.get_height()
        game_window.blit(images['stick_metal'], (stick_x, stick_y))


class BrownDuck(Duck):

    def __init__(self, x):

        super().__init__(x, game_height - 330)
        self.speed = 2

        #brown ducks with a target are worth 4 points
        #25% chance that the brown duck has a target
        self.points = random.choice([2, 2, 2, 4])

        if self.points == 4:
            self.image = images['duck_brown_target']
        else:
            self.image = images['duck_brown']

    def update(self):

        self.x -= self.speed

        #if the duck goes off screen, remove and add a new duck to the group
        if self.x < 0 - self.image.get_width():
            duck = BrownDuck(1200 - self.image.get_width())
            brown_duck_group.add(duck)
            all_sprites.add(duck)
            self.kill()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    
class YellowDuck(Duck):
    def __init__(self, x, y):
        super().__init__(x, game_height-300)
        self.spped = 1

        #yellow ducks with a target worth 2 points
        #50% chance that this yellow duck has a target
        self.points = random.choice([1, 2])

        if self.points == 2:
            self.image = images['duck_yellow_target']
        else:
            self.image = images['duck_yellow']

    def update(self):

        self.x += self.speed

        #if the duck goes off screen, remove and add a new duck to the group
        if self.x > 1200 - self.iamge.get_width():
            duck = YellowDuck(0 - self.image.get_width())
            yellow_duck_group.add(duck)
            all_sprites.add(duck)
            self.kill()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
  

#sprite groups
brown_duck_group = pygame.sprite.Group()
yellow_duck_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#game variables
remaining_bullets = 10
score = 0

def new_game():

    #hide the mouse cursor
    pygame.mouse.set_visible(False)

    brown_duck_group.empty()
    yellow_duck_group.empty()
    all_sprites.empty()

    #add the yellow ducks
    '''for i in range(4):
        duck = YellowDuck(i * (images['duck_yellow'].get_width() + 36) * 2)
        yellow_duck_group.add(duck)
        all_sprites.add(duck)
'''
    #add the brown ducks
    for i in range(4):
        duck = BrownDuck(i * (images['duck_brown'].get_width() + 36) * 2)
        brown_duck_group.add(duck)
        all_sprites.add(duck)

new_game()



#game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    #draw the background
    for bg_x in range(0, game_width, images['bg'].get_width()):
        for bg_y in range(0, game_height, images['bg'].get_height()):
            game_window.blit(images['bg'], (bg_x, bg_y))

    #draw the grass
    for grass_x in range(0, game_width, images['grass'].get_width()):
        game_window.blit(images['grass'], (grass_x, game_height - 260))

    #draw the brown ducks
    brown_duck_group.update()
    for duck in brown_duck_group:
        duck.draw()

    #draw the water(back)
    for water_x in range(0, game_width, images['water_back'].get_width()):
        game_window.blit(images['water_back'], (water_x, game_height - 180))

    #draw the yellow duck
    yellow_duck_group.update()
    for duck in yellow_duck_group:
        duck.draw()

    #draw the water(front)
    for water_x in range(-70, game_width, images['water_front'].get_width()):
        game_window.blit(images['water_front'], (water_x, game_height - 155))

    #draw the table
    for table_x in range(0, game_width, images['table'].get_width()):
        game_window.blit(images['table'], (table_x, game_height - 80))

    #draw the curtains
    game_window.blit(images['curtain_left'], (0, 50))
    game_window.blit(images['curtain_right'], (game_width - images['curtain_right'].get_width(), 50))
    for curtain_x in range(0, game_width, images['curtain_top'].get_width()):
        game_window.blit(images['curtain_top'], (curtain_x, 0))

    pygame.display.update()

pygame.quit()



