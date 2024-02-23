from Card import Card
from random import randint


class Deck:

    def __init__(self, ranks, suits):

        cards = []

        for rank in ranks:
            for suit in suits:
                cards.append(Card(suit, rank))

        self.cards = cards
        self.size = len(cards)


    def draw(self):

        i = randint(0, self.size - 1)
        card = self.cards[i]
        self.size -= 1

        self.cards.remove(card)

        return card

