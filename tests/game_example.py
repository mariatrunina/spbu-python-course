import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.game import Game


def main():
    game = Game(max_steps=5)
    game.start_game()


if __name__ == "__main__":
    main()
