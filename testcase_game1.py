import unittest
import pygame
from unittest.mock import Mock

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



# Create a mock gameover image
game1_gameover_image = Mock()
game1_gameover_image.get_width.return_value = 200

# Create a mock images dictionary
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


if __name__ == '__main__':
   unittest.main()