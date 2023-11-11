import unittest
from game1 import display_score

'''class TestDisplayScore(unittest.TestCase):
   def test_display_score(self):
       # Test code will go here'''
from unittest.mock import patch
class TestDisplayScore(unittest.TestCase):
   @patch('game1.game_window.blit')
   @patch('game1.images.get_width')
   def test_display_score(self, mock_get_width, mock_blit):
       # Set up mock_get_width to return specific values
       mock_get_width.side_effect = [10, 5]

       # Call the function we're testing
       display_score()
       
       images = {}
       # Make assertions about the expected outcome
       mock_blit.assert_any_call(images['score'], (5,5))
       mock_blit.assert_any_call(images['colon'], (15, 5))
       mock_blit.assert_any_call(images['0'], (20, 5))

if __name__ == '__main__':
   unittest.main()