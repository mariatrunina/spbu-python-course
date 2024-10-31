import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cgame import Game


def main():
    game = Game(max_steps=5)  # Создаем экземпляр игры с максимальным количеством шагов
    game.start_game()  # Запускаем игру


if __name__ == "__main__":
    main()
