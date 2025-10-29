# snake_view.py
import time
import turtle
from snake_logic import SnakeGame

class SnakeView:
    def __init__(self, game: SnakeGame):
        self.game = game
        self.setup_screen()
        self.create_objects()
        self.bind_keys()
        self.update_display()

    def setup_screen(self):
        self.wn = turtle.Screen()
        self.wn.title("Snake Game Refactored by Ion Tacu")
        self.wn.bgcolor("green")
        self.wn.setup(width=self.game.width, height=self.game.height)
        self.wn.tracer(0)

    def create_objects(self):
        # Head
        self.head_turtle = turtle.Turtle()
        self.head_turtle.speed(0)
        self.head_turtle.shape("square")
        self.head_turtle.color("black")
        self.head_turtle.penup()

        # Food
        self.food_turtle = turtle.Turtle()
        self.food_turtle.speed(0)
        self.food_turtle.shape("circle")
        self.food_turtle.color("red")
        self.food_turtle.penup()

        # Segments
        self.segment_turtles = []

        # Score display
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, self.game.height // 2 - 40)

    def bind_keys(self):
        self.wn.listen()
        #wsad
        self.wn.onkeypress(lambda: self.game.set_direction("up"), "w")
        self.wn.onkeypress(lambda: self.game.set_direction("down"), "s")
        self.wn.onkeypress(lambda: self.game.set_direction("left"), "a")
        self.wn.onkeypress(lambda: self.game.set_direction("right"), "d")

        #arows
        self.wn.onkeypress(lambda: self.game.set_direction("up"), "Up")
        self.wn.onkeypress(lambda: self.game.set_direction("down"), "Down")
        self.wn.onkeypress(lambda: self.game.set_direction("left"), "Left")
        self.wn.onkeypress(lambda: self.game.set_direction("right"), "Right")

    def update_display(self):
        # Update head
        self.head_turtle.goto(*self.game.head)

        # Update food
        self.food_turtle.goto(*self.game.food)

        # Update segments
        while len(self.segment_turtles) < len(self.game.segments):
            seg = turtle.Turtle()
            seg.speed(0)
            seg.shape("square")
            seg.color("grey")
            seg.penup()
            self.segment_turtles.append(seg)

        for i, pos in enumerate(self.game.segments):
            self.segment_turtles[i].goto(*pos)

        # Hide extra segments (if any were removed)
        for i in range(len(self.game.segments), len(self.segment_turtles)):
            self.segment_turtles[i].goto(1000, 1000)

        # Update score
        self.pen.clear()
        self.pen.write(f"Score: {self.game.score}  High Score: {self.game.high_score}",
                       align="center", font=("Courier", 24, "normal"))

    def game_over(self):
        self.game.reset()
        # Hide all segments
        for seg in self.segment_turtles:
            seg.goto(1000, 1000)
        self.segment_turtles.clear()

    def mainloop(self):
        try:
            while True:
                self.wn.update()

                if self.game.check_food_collision():
                    self.game.grow()
                    self.game.update_food()
                    self.game.update_score()

                self.game.move()

                if self.game.check_border_collision() or self.game.check_self_collision():
                    self.game_over()

                self.update_display()
                turtle.time.sleep(self.game.delay)
        except turtle.Terminator:
            pass  # Graceful exit when window is closed