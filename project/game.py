from typing import List, Optional, Callable
import random


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        """
        Initialize a card with a given rank and suit.

        Args:
            rank (str): The rank of the card (e.g., 'A', '2', 'J').
            suit (str): The suit of the card (e.g., 'Hearts', 'Diamonds').
        """
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        """
        Get the value of the card for scoring purposes.

        Returns:
            int: The value of the card.
        """
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:
    def __init__(self) -> None:
        """
        Initialize a deck of cards with all possible ranks and suits.
        """
        self._cards: List[Card] = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]

        # Create a deck of cards
        for suit in suits:
            for rank in ranks:
                self._cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        """
        Shuffle the deck of cards.
        """
        random.shuffle(self._cards)

    def deal(self) -> Optional[Card]:
        """
        Deal a card from the deck.

        Returns:
            Card: The card dealt, or None if the deck is empty.
        """
        return self._cards.pop() if self._cards else None


class Bet:
    def __init__(self, amount: int):
        """
        Initialize a bet for a game round.

        Args:
            amount (int): The amount of the bet.
        """
        self.amount = amount
