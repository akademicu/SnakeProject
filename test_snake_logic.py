import unittest
from unittest.mock import patch, mock_open
import os
from snake_logic import SnakeGame

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.game = SnakeGame(width=600, height=600)

    def test_initial_state(self):
        self.assertEqual(self.game.head, (0, 0))
        self.assertEqual(self.game.direction, "stop")
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.segments), 0)
        self.assertFalse(self.game.growing)

    def test_direction_control(self):
        self.game.set_direction("up")
        self.assertEqual(self.game.direction, "up")
        self.game.set_direction("down")  # Should be ignored (opposite)
        self.assertEqual(self.game.direction, "up")

        self.game.set_direction("left")
        self.assertEqual(self.game.direction, "left")
        self.game.set_direction("right")  # ignored
        self.assertEqual(self.game.direction, "left")

    def test_move_up(self):
        self.game.set_direction("up")
        self.game.move()
        self.game.move()
        self.assertEqual(self.game.head, (0, 40))

    def test_move_down(self):
        self.game.set_direction("down")
        self.game.move()
        self.assertEqual(self.game.head, (0, -20))

    def test_grow_and_segments(self):
        # Initial state
        self.assertEqual(self.game.head,(0,0))
        self.assertEqual(len(self.game.segments),0)

        # Simulate eating food
        self.game.grow()
        self.assertTrue(self.game.growing)

        # Move once → should add a segment at old head (0,0)
        self.game.set_direction("up")
        self.game.move()
        self.assertEqual(self.game.head,(0,20))
        self.assertEqual(len(self.game.segments),1)
        self.assertEqual(self.game.segments[0],(0,0)) #old head

        # Move again (no grow) → segment count stays 1
        self.game.move()
        self.assertEqual(self.game.head, (0, 40))
        self.assertEqual(len(self.game.segments), 1)
        self.assertEqual(self.game.segments[0], (0, 20)) ## shifted

    def test_border_collision(self):
        # Inside boundary: no collision
        self.game.head = (290, 0)
        self.assertFalse(self.game.check_border_collision())

        # Outside: collision
        self.game.head = (300, 0)
        self.assertTrue(self.game.check_border_collision())

        self.game.head = (-300, 0)
        self.assertTrue(self.game.check_border_collision())

        self.game.head = (0, 295)
        self.assertTrue(self.game.check_border_collision())

    def test_self_collision(self):
        self.game.head = (0, 0)
        self.game.segments = [(20, 0), (0, 0)]  # head overlaps segment
        self.assertTrue(self.game.check_self_collision())

        self.game.segments = [(20, 0)]
        self.assertFalse(self.game.check_self_collision())

    def test_food_collision(self):
        self.game.head = (40, 40)
        self.game.food = (40, 40)
        self.assertTrue(self.game.check_food_collision())

        self.game.food = (60, 60)
        self.assertFalse(self.game.check_food_collision())

    def test_update_score_and_high_score(self):
        initial_high = self.game.high_score
        self.game.score = 50
        self.game.update_score()  # +10 → 60
        self.assertEqual(self.game.score, 60)

        # If it beats high score, update it
        if 60 > initial_high:
            self.assertEqual(self.game.high_score, 60)

    @patch("snake_logic.os.path.exists")
    @patch("snake_logic.open", new_callable=mock_open, read_data='{"high_score": 150}')
    def test_load_high_score_success(self, mock_file, mock_exists):
        mock_exists.return_value = True
        game = SnakeGame()
        self.assertEqual(game.high_score, 150)

    @patch("snake_logic.os.path.exists")
    @patch("snake_logic.open", new_callable=mock_open, read_data='{"high_score": "valid"}')
    def test_load_high_score_corrupted(self, mock_file, mock_exists):
        mock_exists.return_value = True
        game = SnakeGame()
        print(game.high_score)
        self.assertEqual(game.high_score, 0)

    @patch("snake_logic.os.path.exists")
    def test_load_high_score_not_exists(self, mock_exists):
        mock_exists.return_value = False
        game = SnakeGame()
        self.assertEqual(game.high_score, 0)

    # @patch("snake_logic.open", new_callable=mock_open)
    # def test_save_high_score(self, mock_file):
    #     self.game.high_score = 200
    #     self.game.save_high_score()
    #     mock_file.assert_called_with("highscore.json", "w")
    #     mock_file().write.assert_called_once()

if __name__ == '__main__':
    unittest.main()