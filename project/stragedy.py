from game import Deck
from bot import Bot
import random
from typing import List


class Strategy:
    @staticmethod
    def aggressive(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        """
        Aggressive strategy: Hit if the hand value is less than 17.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.
            bet_history (List[int]): The history of bets made by the bot.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return bot.hand.calculate_value() < 17

    @staticmethod
    def cautious(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        """
        Cautious strategy: Hit if the hand value is less than 15.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.
            bet_history (List[int]): The history of bets made by the bot.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return bot.hand.calculate_value() < 15

    @staticmethod
    def random(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        """
        Random strategy: Hit or stand randomly.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.
            bet_history (List[int]): The history of bets made by the bot.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return random.choice([True, False])

    @staticmethod
    def historical_strategy(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        """
        Strategy considering the bet history:
        If the last bet was high, stand if the hand value is 17 or greater, otherwise hit.
        If the last bet was low or nonexistent, follow the aggressive strategy.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.
            bet_history (List[int]): The history of bets made by the bot.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        if bet_history and bet_history[-1] > 10:  # Пример условия для высоких ставок
            return (
                bot.hand.calculate_value() < 17
            )  # Агрессивная игра на высоких ставках
        else:
            return bot.hand.calculate_value() < 15  # Осторожная игра на низких ставках
