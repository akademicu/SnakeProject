# main.py
from snake_logic import SnakeGame
from snake_view import SnakeView

if __name__ == "__main__":
    game = SnakeGame(width=600, height=600)
    view = SnakeView(game)
    view.mainloop()