from Game import Game
from Player import Player
from random import randint, choice

# Game variant with all cards allready drawn
# 4+ players advised

class GameNodeckRandom(Game):
    
    def __init__(self, ranks: list, suits: list, players: Player):
        super().__init__(ranks, suits, players)

    def start(self):
        self.log = []
        self.current_player_id = 0

        for player in self._players:
            for _ in range(len(self.ranks) * len(self.suits) / len(self._players)):
                player.add_card(self._deck.draw())
            
            self.check_for_chests(player)


        for player in self._players:
            print(player.cards)

