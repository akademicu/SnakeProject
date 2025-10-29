# snake_logic.py
import random
import json
import os

HIGHSCORE_FILE = "highscore.json"

class SnakeGame:
    def __init__(self, width=600, height=600, grid_size=20):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.boundary = width // 2 - grid_size // 2
        self.load_high_score()
        self.reset()

    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    data = json.load(f)
                    hs =data.get("high_score", 0)
                    if isinstance(hs, int) and hs >= 0:
                        self.high_score = hs
                    else:
                        self.high_score = 0
            except (json.JSONDecodeError, KeyError, TypeError, ValueError, IOError):
                self.high_score = 0
        else:
            self.high_score = 0

    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def reset(self):
        self.head = (0, 0)
        self.direction = "stop"
        self.segments = []
        self.score = 0
        self.delay = 0.1
        self.food = self._random_food_position()
        self.growing = False  # ← NEW: tracks if we should grow this frame

    def _random_food_position(self):
        max_coord = self.boundary
        x = random.randint(-max_coord, max_coord)
        y = random.randint(-max_coord, max_coord)
        x = round(x / self.grid_size) * self.grid_size
        y = round(y / self.grid_size) * self.grid_size
        return (x, y)

    def set_direction(self, new_dir):
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if new_dir in opposites and self.direction != opposites[new_dir]:
            self.direction = new_dir

    def move(self):
        if self.direction == "stop":
            return

        x, y = self.head
        if self.direction == "up":
            y += self.grid_size
        elif self.direction == "down":
            y -= self.grid_size
        elif self.direction == "left":
            x -= self.grid_size
        elif self.direction == "right":
            x += self.grid_size

        new_head = (x, y)

        if self.growing:
            # Keep all segments + add current head as new segment
            self.segments = [self.head] + self.segments
            self.growing = False
        else:
            # Normal move: shift segments, drop last
            if self.segments:
                self.segments = [self.head] + self.segments[:-1]
            # else: no body, just move head

        self.head = new_head

    def grow(self):
        self.growing = True  # ← Signal to keep tail on next move

    def check_border_collision(self):
        x, y = self.head
        return x > self.boundary or x < -self.boundary or y > self.boundary or y < -self.boundary

    def check_self_collision(self):
        return self.head in self.segments

    def check_food_collision(self):
        return self.head == self.food

    def update_food(self):
        self.food = self._random_food_position()
        while self.food in self.segments or self.food == self.head:
            self.food = self._random_food_position()

    def update_score(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.delay = max(0.02, self.delay - 0.001)