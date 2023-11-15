import unittest
import pygame
from unittest.mock import Mock, patch
from game1 import YellowDuck, BrownDuck, images, game_window, display_score
from pygame.sprite import Group
from pygame import Surface
from pygame.locals import MOUSEBUTTONDOWN

def handle_events(events):
    gameover = True
    running = False
    remaining_bullets = 0
    score = 0
    for event in events:
        if event.type == pygame.QUIT:
           gameover = False
           running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
           gameover = False
           running = True
           remaining_bullets = 10
           score = 0

    return gameover, running, remaining_bullets, score

class TestGameLoop(unittest.TestCase):
    def test_quit_event(self):
       quit_event = pygame.event.Event(pygame.QUIT)
       gameover, running, remaining_bullets, score  = handle_events([quit_event])
       self.assertFalse(gameover)
       self.assertFalse(running)

    def test_mousebuttondown_event(self):
       mousebuttondown_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
       gameover, running, remaining_bullets, score = handle_events([mousebuttondown_event])
       self.assertFalse(gameover)
       self.assertTrue(running)
       self.assertEqual(remaining_bullets, 10)
       self.assertEqual(score, 0)
       
game1_gameover_image = Mock()
game1_gameover_image.get_width.return_value = 200

mock_images = {'gameover': game1_gameover_image}

def gameover_image(game_width, images):
    gameover = images['gameover']
    gameover_width = gameover.get_width()
    gameover_x = (game_width - gameover_width) // 2
    gameover_y = 100
    return gameover_x, gameover_y

class TestGameoverImage(unittest.TestCase):
    def test_gameover_image(self):
        game_width = 800
        gameover_x, gameover_y = gameover_image(game_width, mock_images)
        self.assertEqual(gameover_x, 300)
        self.assertEqual(gameover_y, 100)

class TestYellowDuck(unittest.TestCase):
    def setUp(self):
        self.yellow_duck_group = Group()
        self.all_sprites = Group()
        self.images = {'duck_yellow': Surface((10, 10))} 

    def test_add_duck_to_group(self):
        duck = YellowDuck(0)
        self.yellow_duck_group.add(duck)
        self.all_sprites.add(duck)
        self.assertIn(duck, self.yellow_duck_group)
        self.assertIn(duck, self.all_sprites)

class TestBrownDuck(unittest.TestCase):
    def setUp(self):
         self.brown_duck_group = Group()
         self.all_sprites = Group()
         self.image = Surface((10, 10)) 

    def test_add_brown_duck_to_group(self):
         duck = BrownDuck(1200 - self.image.get_width())
         self.brown_duck_group.add(duck)
         self.all_sprites.add(duck)
         self.assertIn(duck, self.brown_duck_group)
         self.assertIn(duck, self.all_sprites)

def display_score(game_window, images, score):
   print(score)

class TestDisplayScore(unittest.TestCase):
    def setUp(self):
       self.game_window = Surface((800, 600))
       self.images = {'score': Surface((10, 10)), 'colon': Surface((10, 10))} 

    def test_display_score(self):
       self.score = 1234
       display_score(self.game_window, self.images, self.score)
       self.assertEqual(self.score, 1234)

class Sprite:
    def __init__(self, points):
        self.is_hit = False
        self.points = points
        self.rect = pygame.Rect(0, 0, 10, 10)


def handle_mouse_click(event, all_sprites, remaining_bullets, score):
    if event.type == MOUSEBUTTONDOWN:
        remaining_bullets -= 1
        click_x, click_y = event.pos
        for sprite in all_sprites:
            if sprite.is_hit == False and sprite.rect.collidepoint(click_x, click_y):
                sprite.is_hit = True
                score += sprite.points
                break
    return remaining_bullets, score, all_sprites

class TestHandleMouseClick(unittest.TestCase):
    def test_handle_mouse_click(self):
        pygame.init() 
        all_sprites = [Sprite(100) for _ in range(5)]
        remaining_bullets = 5
        score = 0

        event = pygame.event.Event(MOUSEBUTTONDOWN, {'pos': (5, 5)})
        remaining_bullets, score, all_sprites = handle_mouse_click(event, all_sprites, remaining_bullets, score)

        self.assertEqual(remaining_bullets, 4)
        self.assertEqual(score, 100)
        self.assertTrue(all_sprites[0].is_hit)  

if __name__ == '__main__':
   unittest.main()