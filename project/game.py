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
        self._cards: List[Card] = []  # Приватный атрибут, содержащий карты
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
