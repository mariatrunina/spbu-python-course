from typing import List
from game import Card


class BotHand:
    def __init__(self) -> None:
        """
        Initialize an empty hand for the bot.
        """
        self._cards: List[Card] = []  # Приватный атрибут, содержащий карты бота

    def add_card(self, card: Card) -> None:
        """
        Add a card to the bot's hand.

        Args:
            card (Card): The card to add.
        """
        self._cards.append(card)

    def reset(self) -> None:
        """
        Resets the bot's hand for a new round.
        """
        self._cards.clear()

    def calculate_value(self) -> int:
        """
        Calculate the total value of the hand, accounting for Aces.

        Returns:
            int: The calculated value of the hand.
        """
        value = sum(card.value() for card in self._cards)
        aces = sum(1 for card in self._cards if card.rank == "A")

        # Adjust for Aces if necessary
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def is_busted(self) -> bool:
        """
        Check if the bot has busted (i.e., the hand value is over 21).

        Returns:
            bool: True if the bot has busted, otherwise False.
        """
        return self.calculate_value() > 21
