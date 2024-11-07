import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем классы из папки project
from project.game import Card, Bet, Deck, Strategy, Bot, BotHand, Game


@pytest.fixture
def setup_game():
    deck = Deck()
    game = Game(max_steps=1)
    return deck, game


def test_deck_initialization(setup_game):
    deck, _ = setup_game
    assert len(deck._cards) == 52


def test_deck_shuffle(setup_game):
    deck, _ = setup_game
    original_deck = deck._cards.copy()
    deck.shuffle()
    assert original_deck != deck._cards


def test_dealing_cards(setup_game):
    deck, _ = setup_game
    initial_count = len(deck._cards)
    dealt_card = deck.deal()
    assert len(deck._cards) == initial_count - 1
    assert dealt_card is not None


def test_bot_hand_initialization():
    bot = Bot("TestBot", Strategy.aggressive)
    assert len(bot.hand._cards) == 0


def test_bot_add_card(setup_game):
    deck, game = setup_game
    bot = Bot("TestBot", Strategy.aggressive)
    card = deck.deal()
    bot.hand.add_card(card)
    assert len(bot.hand._cards) == 1


def test_calculate_hand_value():
    bot = Bot("TestBot", Strategy.aggressive)
    bot.hand.add_card(Card("A", "Hearts"))
    bot.hand.add_card(Card("K", "Diamonds"))
    value = bot.hand.calculate_value()
    assert value == 21


def test_aggressive_strategy(setup_game):
    deck, _ = setup_game
    bot = Bot("AggressiveBot", Strategy.aggressive)
    bot.hand.add_card(Card("10", "Hearts"))
    assert (
        bot._strategy(bot, deck, []) is True
    )  # передаем пустой список вместо bot._bet_history
    bot.hand.add_card(Card("6", "Diamonds"))
    assert bot._strategy(bot, deck, []) is True
    bot.hand.add_card(Card("5", "Clubs"))
    assert bot._strategy(bot, deck, []) is False


def test_game_round(setup_game):
    deck, game = setup_game
    initial_deck_size = len(deck._cards)
    game.start_game()
    expected_min_cards_left = initial_deck_size - 6
    assert len(deck._cards) >= expected_min_cards_left - 2


def test_show_hands(setup_game):
    _, game = setup_game
    try:
        game._show_hands()
    except Exception as e:
        pytest.fail(f"_show_hands raised {type(e).__name__} unexpectedly!")


def test_game_state_change(setup_game):
    _, game = setup_game
    initial_step = game._current_step
    game.start_game()
    assert game._current_step > initial_step


def test_bet_initialization():
    bet = Bet(10)
    assert bet.amount == 10


def test_betting_system(setup_game):
    deck, game = setup_game
    bot = game._bots[0]
    initial_bet = 10
    bot.place_bet(initial_bet)
    assert bot.current_bet is not None
    assert bot.current_bet.amount == initial_bet


def test_bot_hand_reset():
    hand = BotHand()
    hand.add_card(Card("A", "Hearts"))
    hand.add_card(Card("5", "Diamonds"))
    assert hand.calculate_value() == 16
    hand.reset()
    assert hand.calculate_value() == 0


def test_is_busted():
    hand = BotHand()
    hand.add_card(Card("K", "Hearts"))
    hand.add_card(Card("Q", "Diamonds"))
    hand.add_card(Card("2", "Clubs"))
    assert hand.is_busted() is True


def test_multiple_bets_each_round(setup_game):
    deck, game = setup_game
    bot = game._bots[0]
    bot.place_bet(10)
    assert bot.current_bet.amount == 10

    bot.place_bet(15)
    assert bot.current_bet.amount == 15


if __name__ == "__main__":
    pytest.main()
