from typing import List, Optional, Callable
import random


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:
    def __init__(self) -> None:
        self._cards: List[Card] = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
        for suit in suits:
            for rank in ranks:
                self._cards.append(Card(rank, suit))

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def deal(self) -> Optional[Card]:
        return self._cards.pop() if self._cards else None


class Bet:
    def __init__(self, amount: int):
        self.amount = amount


class BotHand:
    def __init__(self) -> None:
        self._cards: List[Card] = []
        self._points: int = 0  # Инициализация очков

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def reset(self) -> None:
        self._cards = []  # Сбрасываем карты
        self._points = 0  # Сбрасываем очки

    def calculate_value(self) -> int:
        value = sum(card.value() for card in self._cards)
        aces = sum(1 for card in self._cards if card.rank == "A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def is_busted(self) -> bool:
        return self.calculate_value() > 21


class Bot:
    def __init__(
        self, name: str, strategy: Callable[["Bot", Deck, List[int]], bool]
    ) -> None:
        self.name = name
        self.hand = BotHand()
        self._strategy = strategy
        self.current_bet: Optional[Bet] = None
        self.is_active: bool = True

    def play(self, deck: Deck) -> None:
        while self._strategy(self, deck, []) and self.is_active:
            card = deck.deal()
            if card:
                self.hand.add_card(card)
                print(
                    f"{self.name}'s hand value after adding card: {self.hand.calculate_value()}"
                )
                if self.hand.is_busted():
                    print(f"{self.name} busts!")
                    self.is_active = False
                    break

    def place_bet(self, amount: int) -> None:
        self.current_bet = Bet(amount)
        print(f"{self.name} placed a bet of {amount}.")


class Strategy:
    @staticmethod
    def aggressive(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        return bot.hand.calculate_value() < 17

    @staticmethod
    def cautious(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        return bot.hand.calculate_value() < 15

    @staticmethod
    def random(bot: Bot, deck: Deck, bet_history: List[int]) -> bool:
        return random.choice([True, False])


class Game:
    def __init__(self, max_steps: int = 10) -> None:
        self._deck = Deck()
        self._deck.shuffle()
        self._bots = [
            Bot("Bot1", Strategy.aggressive),
            Bot("Bot2", Strategy.cautious),
            Bot("Bot3", Strategy.random),
        ]
        self._max_steps = max_steps
        self._current_step = 0

    def start_game(self) -> None:
        while self._current_step < self._max_steps:
            print(f"\n--- Round {self._current_step + 1} ---")
            self.play_round()
            self._current_step += 1
            self._show_hands()

    def play_round(self) -> None:
        for bot in self._bots:
            if not bot.is_active:
                continue  # Игнорируем проигравших игроков

            bet_amount = random.randint(1, 20)
            bot.place_bet(bet_amount)

            # Раздаем 2 карты каждому боту
            for _ in range(2):
                card = self._deck.deal()
                if card:
                    bot.hand.add_card(card)

            print(
                f"{bot.name}'s hand: {[f'{card.rank} of {card.suit}' for card in bot.hand._cards]}"
            )
            bot.play(self._deck)

            if bot.hand.is_busted():
                print(f"{bot.name} busted with value {bot.hand.calculate_value()}")
                bot.is_active = False  # Выбывает из игры

        self.reset_bot_scores()  # Обнуляем карты и очки всех ботов

    def reset_bot_scores(self) -> None:
        for bot in self._bots:
            if bot.is_active:
                bot.hand.reset()  # Сбрасываем карты и очки только активных ботовивных ботов

    def _show_hands(self) -> None:
        for bot in self._bots:
            if bot.is_active:
                print(f"{bot.name}'s hand value: {bot.hand.calculate_value()}")
            else:
                print(f"{bot.name} is out of the game.")
