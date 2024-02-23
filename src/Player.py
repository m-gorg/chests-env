class Player:
    def __init__(self, id):
        self.cards: list = []
        self.chests = []
        self.id = id
        self.suits = None
        self.ranks = None


    def add_card(self, card):
        self.cards.append(card)


    def remove_card(self, card):
        if card not in self.cards:
            raise Exception(f"Player {self.id} doesn't have {card}")
        
        self.cards.remove(card)


    def get_turn(self, game, target):
        
        raise NotImplementedError

