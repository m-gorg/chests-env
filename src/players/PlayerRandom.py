from Player import Player
from random import randint, sample
from Turn import Turn

class PlayerRandom(Player):

    def __init__(self, id):
        super().__init__(id)


    def get_turn(self, game, target):

        target = target
        rank = self.cards[randint(0, len(self.cards)) - 1].rank
        count = randint(1, 3)
        suits = sample(self.suits, count)

        return Turn(target, rank, count, suits)