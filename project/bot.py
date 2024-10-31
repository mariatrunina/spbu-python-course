from typing import List, Optional, Callable
from game import Deck, Bet
from bothand import BotHand


class Bot:

    def __init__(
        self, name: str, strategy: Callable[["Bot", Deck, List[int]], bool]
    ) -> None:
        """
        Initialize a bot with a name and a strategy for playing.

        Args:
            name (str): The name of the bot.
            strategy (Callable[["Bot", Deck, List[int]], bool]): The strategy function for the bot.
        """
        self.name = name
        self.hand = BotHand()
        self._strategy = strategy
        self._bet_history: List[int] = []
        self.current_bet: Optional[Bet] = None
        self.is_active: bool = True

    def play(self, deck: Deck) -> None:
        while self._strategy(self, deck, self._bet_history):
            card = deck.deal()
            if card:
                self.hand.add_card(card)
                print(f"Hand value after adding card: {self.hand.calculate_value()}")
                if self.hand.is_busted():
                    print(f"Busted! Setting is_active to False.")
                    self.is_active = False
                    break

    def place_bet(self, amount: int) -> None:
        """
        Place a bet for the bot.

        Args:
            amount (int): The amount of the bet.
        """
        self.current_bet = Bet(amount)
        self._bet_history.append(amount)
        print(f"{self.name} placed a bet of {amount}.")
