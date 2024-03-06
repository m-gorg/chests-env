
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.as_tuple = (rank, suit)


    def __eq__(self, card):
        
        if self.suit == card.suit and self.rank == card.rank:
            return True
        
        return False
    

    def __str__(self) -> str:
        return self.rank + self.suit

