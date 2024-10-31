from game import Deck
from stragedy import Strategy
from bot import Bot
from bothand import BotHand
import random


class Game:
    def __init__(self, max_steps: int = 10) -> None:
        """
        Initialize the game with a deck of cards and bots.

        Args:
            max_steps (int): The maximum number of steps to play.
        """
        self._deck = Deck()  # Приватный атрибут для колоды
        self._deck.shuffle()
        self._bots = [
            Bot("Bot1", Strategy.aggressive),
            Bot("Bot2", Strategy.cautious),
            Bot("Bot3", Strategy.random),
            Bot(
                "Bot4", Strategy.historical_strategy
            ),  # Новый бот с исторической стратегией
        ]
        self._max_steps = (
            max_steps  # Приватный атрибут для максимального количества шагов
        )
        self._current_step = 0  # Приватный атрибут для текущего шага

    def start_game(self) -> None:
        """
        Start the game and control the flow of rounds.
        """
        while self._current_step < self._max_steps:
            print(f"\n--- Round {self._current_step + 1} ---")
            self.play_round()
            self._current_step += 1
            self._show_hands()
            self.reset_bots_hands()  # Обнуляем руки всех ботов после раунда

    def play_round(self) -> None:
        """
        Play a round, dealing cards to all bots and allowing them to play.
        """
        for bot in self._bots:
            if not bot.is_active:
                print(f"{bot.name} is out of the game and will not place a bet.")
                continue

            bet_amount = random.randint(1, 20)  # Генерируем случайную ставку
            bot.place_bet(bet_amount)  # Бот ставит ставку

            card1 = self._deck.deal()
            if card1 is not None:
                bot.hand.add_card(card1)
            else:
                print(
                    f"{bot.name} cannot receive more cards. No cards left in the deck."
                )
                return

            card2 = self._deck.deal()
            if card2 is not None:
                bot.hand.add_card(card2)
            else:
                print(
                    f"{bot.name} cannot receive more cards. No cards left in the deck."
                )
                return

            print(
                f"{bot.name}'s hand: {[card.rank + ' of ' + card.suit for card in bot.hand._cards]}"
            )

            # Позволяем боту играть на своем ходу
            bot.play(self._deck)

            if bot.hand.is_busted():
                print(
                    f"{bot.name} busts with value {bot.hand.calculate_value()}. He is out of the game."
                )
                bot.is_active = False  # Бот выбывает из игры

    def reset_bots_hands(self):
        """
        Reset all bots’ hands for the next round.
        """
        for bot in self._bots:
            bot.hand.reset()

    def _show_hands(self) -> None:
        """
        Display the current hands and values of all bots.
        """
        for bot in self._bots:
            if bot.is_active:
                print(f"{bot.name}'s hand value: {bot.hand.calculate_value()}")
