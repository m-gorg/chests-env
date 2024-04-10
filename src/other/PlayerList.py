from Player import Player

class Node:
    
    def __init__(self, player):
        self.player: Player = player
        self.next: Node = None


class PlayerList:

    def __init__(self, players):
        pl = [Node(player) for player in players]

        for i in range(len(pl)):
            pl[i - 1].next = pl[i]

    
    




