import random
from typing import List, Optional, Callable


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
        self.cards: List[Card] = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]

        # Create a deck of cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        """
        Shuffle the deck of cards.
        """
        random.shuffle(self.cards)

    def deal(self) -> Optional[Card]:
        """
        Deal a card from the deck.

        Returns:
            Card: The card dealt, or None if the deck is empty.
        """
        return self.cards.pop() if self.cards else None


class Bot_Hand:
    def __init__(self) -> None:
        """
        Initialize an empty hand for the bot.
        """
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        """
        Add a card to the bot's hand.

        Args:
            card (Card): The card to add.
        """
        self.cards.append(card)

    def calculate_value(self) -> int:
        """
        Calculate the total value of the hand, accounting for Aces.

        Returns:
            int: The calculated value of the hand.
        """
        value = sum(card.value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")

        # Adjust for Aces if necessary
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value


class Bot:
    def __init__(self, name: str, strategy: Callable[["Bot", Deck], bool]) -> None:
        self.name = name
        self.hand = Bot_Hand()
        self.strategy = strategy

    def play(self, deck: Deck) -> None:
        while self.strategy(self, deck):
            print(f"{self.name} decides to hit.")
            card = deck.deal()
            if card is not None:
                self.hand.add_card(card)
                print(f"{self.name}'s hand value: {self.hand.calculate_value()}")
            else:
                print(f"{self.name} cannot hit, deck is empty.")
                break


class Game:
    def __init__(self, max_steps: int = 10) -> None:
        """
        Initialize the game with a deck of cards and bots.

        Args:
            max_steps (int): The maximum number of steps to play.
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.bots = [
            Bot("Bot1", self.aggressive_strategy),
            Bot("Bot2", self.cautious_strategy),
            Bot("Bot3", self.random_strategy),
        ]
        self.max_steps = max_steps
        self.current_step = 0

    def start_game(self) -> None:
        """
        Start the game and control the flow of rounds.
        """
        while self.current_step < self.max_steps:
            print(f"\n--- Round {self.current_step + 1} ---")
            self.play_round()
            self.current_step += 1
            self.show_hands()

    def play_round(self) -> None:
        for bot in self.bots:
            card1 = self.deck.deal()
            if card1 is not None:
                bot.hand.add_card(card1)
            else:
                print(
                    f"{bot.name} cannot receive more cards. No cards left in the deck."
                )
                return

            card2 = self.deck.deal()
            if card2 is not None:
                bot.hand.add_card(card2)
            else:
                print(
                    f"{bot.name} cannot receive more cards. No cards left in the deck."
                )
                return

            print(
                f"{bot.name}'s hand: {[card.rank + ' of ' + card.suit for card in bot.hand.cards]}"
            )

    def show_hands(self) -> None:
        """
        Display the current hands and values of all bots.
        """
        for bot in self.bots:
            print(f"{bot.name}'s hand value: {bot.hand.calculate_value()}")

    def aggressive_strategy(self, bot: Bot, deck: Deck) -> bool:
        """
        Aggressive strategy: Hit if the hand value is less than 17.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return bot.hand.calculate_value() < 17

    def cautious_strategy(self, bot: Bot, deck: Deck) -> bool:
        """
        Cautious strategy: Hit if the hand value is less than 15.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return bot.hand.calculate_value() < 15

    def random_strategy(self, bot: Bot, deck: Deck) -> bool:
        """
        Random strategy: Hit or stand randomly.

        Args:
            bot (Bot): The bot using this strategy.
            deck (Deck): The deck of cards being used.

        Returns:
            bool: Whether to hit (True) or not (False).
        """
        return random.choice([True, False])
