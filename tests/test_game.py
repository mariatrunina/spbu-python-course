import pytest
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.game import Card, Deck, Bot_Hand, Bot, Game


@pytest.fixture
def setup_game():

    deck = Deck()
    game = Game(max_steps=1)
    return deck, game


def test_deck_initialization(setup_game):

    deck, _ = setup_game
    assert len(deck.cards) == 52


def test_deck_shuffle(setup_game):

    deck, _ = setup_game
    original_deck = deck.cards.copy()
    deck.shuffle()
    assert original_deck != deck.cards


def test_dealing_cards(setup_game):

    deck, _ = setup_game
    initial_count = len(deck.cards)
    dealt_card = deck.deal()
    assert len(deck.cards) == initial_count - 1
    assert dealt_card is not None


def test_bot_hand_initialization(setup_game):

    _, game = setup_game
    bot = Bot("TestBot", game.aggressive_strategy)
    assert len(bot.hand.cards) == 0


def test_bot_add_card(setup_game):
    deck, game = setup_game  # Добавьте это, чтобы получить доступ к переменной game
    bot = Bot("TestBot", game.aggressive_strategy)
    card = deck.deal()
    bot.hand.add_card(card)
    assert len(bot.hand.cards) == 1


def test_calculate_hand_value(setup_game):

    _, game = setup_game
    bot = Bot("TestBot", game.aggressive_strategy)
    bot.hand.add_card(Card("A", "Hearts"))  # Ace
    bot.hand.add_card(Card("K", "Diamonds"))  # King
    value = bot.hand.calculate_value()
    assert value == 21  # Ace counts as 11 and King counts as 10


def test_aggressive_strategy(setup_game):
    deck, game = setup_game
    bot = Bot("AggressiveBot", game.aggressive_strategy)
    bot.hand.add_card(Card("10", "Hearts"))
    assert bot.strategy(bot, deck) is True
    bot.hand.add_card(Card("6", "Diamonds"))
    assert bot.strategy(bot, deck) is True
    bot.hand.add_card(Card("5", "Clubs"))
    assert bot.strategy(bot, deck) is False


def test_game_round(setup_game):
    deck, game = setup_game
    initial_deck_size = len(deck.cards)
    game.start_game()
    expected_min_cards_left = initial_deck_size - 6
    assert len(game.deck.cards) >= expected_min_cards_left - 2


def test_show_hands(setup_game):

    _, game = setup_game
    try:
        game.show_hands()
    except Exception as e:
        pytest.fail(f"show_hands raised {type(e).__name__} unexpectedly!")


def test_game_state_change(setup_game):

    _, game = setup_game
    initial_step = game.current_step
    game.start_game()
    assert game.current_step > initial_step


if __name__ == "__main__":
    pytest.main()
