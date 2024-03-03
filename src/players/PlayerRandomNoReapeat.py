from Player import Player
from random import randint, sample
from Turn import Turn

# 4 players, game no deck random
# [' 2', ' 3', ' 4', ' 5', ' 6'] ['♠', '♥', '♣', '♦']

class PlayerRandomNoRepeat(Player):

    def __init__(self, id, k=100):
        """
        k = max amount of tries for turn generation
        if k generations fail, turn is repeated
        """
        super().__init__(id)
        self.turns = [dict(zip([' 2', ' 3', ' 4', ' 5', ' 6'], [[] for s in range(5)])) for p in range(3)] # self.turns[target][rank]
        self.k = k


    def get_turn(self, game, target):

        for _ in range(self.k):
            target = target
            rank = self.cards[randint(0, len(self.cards)) - 1].rank
            count = randint(1, 3)
            suit = sample(self.suits, count)

            turn = Turn(target, rank, count, suit)

            flag = True
            for past_turn in self.turns[target][rank]:
                if turn == past_turn:
                    print("turn rejected")
                    flag = False
                    break

            if flag: break

        if not flag:
            self.turns[target][suit].append(turn)

        return turn