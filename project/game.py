import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank  
        self.suit = suit
    
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  
        else:
            return int(self.rank)

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']

     # Создаю цикл для создания колоды
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit)) 
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
    
class Bot_Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = sum(card.value() for card in self.cards)
        
        # Проверяю на туз и коррекцию значения
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
            
        return value
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Bot_Hand()

    def play(self):
        # Логика игры
        pass

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def start_game(self):
        # Раздача карт
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
        
        self.show_hands()

    def show_hands(self):
        print(f"{self.player.name}'s hand: {[card.rank + ' of ' + card.suit for card in self.player.hand.cards]}")
        print(f"{self.dealer.name}'s hand: {[card.rank + ' of ' + card.suit for card in self.dealer.hand.cards]}")