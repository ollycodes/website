import random


SUITS = {'Hearts', 'Diamonds', 'Spades', 'Clubs'}

RANKS = {
    'Ace': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10
    }


def generate_deck(number):
    cards = []

    for num in range(number):
        for suit in SUITS:
            for rank in RANKS:
                cards.append(Card(rank, suit))
    random.shuffle(cards)
    return cards

def generate_player():
    dealer = Player("dealer", [])
    player = str(input('name: '))
    player = Player(player, [])
    return dealer, player

def total(hand):
    hand_total = 0
    has_ace = False
    for card in hand:
        card_value = RANKS.get(card.rank)
        if card_value == 1:
            has_ace = True
        hand_total += card_value

    if hand_total <= 11 and has_ace:
        hand_total += 10
    return hand_total

def show(hand, num=None):
    shown = 0
    for card in hand:
        if shown == num:
            break
        print(f"\t- {card}")
        shown += 1


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

class Blackjack:
    def __init__(self):
        self.deck = generate_deck(2)
        self.dealer, self.player = generate_player()

    def draw_cards(self, number):
        return [self.deck.pop() for _ in range(number)]

    def initial_draw(self):
        self.dealer.hand = list()
        self.dealer.hand += self.draw_cards(2)
        self.player.hand = list()
        self.player.hand += self.draw_cards(2)

    def show_hands(self):
        print(f"{'-' * 20}\n{self.player.name}'s hand:")
        show(self.player.hand)
        print(f"\t- total: {total(self.player.hand)}")
        print("\ndealer's hand")
        show(self.dealer.hand, num=1)

    def prompt_action(self):
        hit = ['h', 'H', 'hit', 'Hit']
        action = str(input('Hit or Stand: '))
        if action in hit:
            self.player.hand += self.draw_cards(1)
            return True
        return False

    def player_turn(self):
        value = total(self.player.hand)
        if value > 21:
            return
        elif value == 21:
            return
        elif value < 21:
            return self.prompt_action()

    def dealers_turn(self):
        if total(self.player.hand) > 21 and total(self.dealer.hand) < 22:
            print("dealer wins!")
            return
        while total(self.dealer.hand) < 17:
            self.dealer.hand += self.draw_cards(1)
        print(f"{'-' * 20}\ndealer's hand")
        show(self.dealer.hand)
        print(f"dealer total: {total(self.dealer.hand)}")

    def compare(self):
        player_total = total(self.player.hand)
        dealer_total = total(self.dealer.hand)
        if player_total == dealer_total:
            print("Draw!")
        elif player_total > dealer_total and player_total <= 21:
            print("Hit!")
        elif dealer_total > 21:
            print("Hit!")
        else:
            print("Bust!")

    def run(self):
        self.initial_draw()
        self.show_hands()
        while self.player_turn():
            self.show_hands()
        self.dealers_turn()
        self.compare()

if __name__ == '__main__':
    game = Blackjack()
    game.run()
