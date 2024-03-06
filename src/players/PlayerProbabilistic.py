from Player import Player
from random import randint
from Turn import Turn
from Card import Card


ranks = [' 2', ' 3', ' 4', ' 5', ' 6']
suits = ['♠', '♥', '♣', '♦']


class PlayerProbabilistic(Player): # not susceptible to bluff
    
    def __init__(self, id):
        super().__init__(id)
        
        self.target_cards = None


    def targets_to_turn(self, targets):
        turn = Turn(targets[0].rank, len(targets), [t.suit for t in targets])
        return turn


    def rel_id(self, x):
        return (x - self.id - 1) % 4
    
    def set_weights(self, card, p):
        for i in range(3):
            self.weights[i][card.as_tuple] = p
    
    def update_weights(self, game):

        for log in game.log[-4:]: # 3 last logs for 3 oponents
            player = self.rel_id(log['player'])
            target = self.rel_id(log['target'])

            if target == 3: # if we were targeted:
                pass #TODO

            match log['responce']:
                case 3: # guessed right
                    
                    for rank in log['turn'].rank:
                        for suit in log['turn'].suits:
                            card = Card(suit, rank)
                            if card not in self.target_cards: # check if we care
                                continue

                            self.set_weights(card, 0) # no one else has the card...
                            self.weights[player][card.as_tuple] = 1 # except the one who guessed the card
                    
                case 2: # wrong suit(s)
                    pass
                case 1: # wroung amount
                    pass
                case 0: # no cards of given rank
                    
                    for suit in game.suits:
                        card = Card(suit, log['turn'].rank)
                        if card not in self.target_cards: # only cards we care about
                            continue
                        
                        #TODO? if len([c for c in self.target_cards if c.rank == log['turn'].rank]) == 1: # if we need only one card
                        
                        for i in range(3):
                            if i == target:
                                self.weights[i][card.as_tuple] = 0 # target has no cards of given rank
                            else:
                                self.weights[i][card.as_tuple] += 1/6 # higher P that others have the card TODO 1/6 ?


    def get_turn(self, game, target_id):
        
        if self.target_cards == None:
            self.target_cards = []

            for rank in ranks:
                if rank not in [_.rank for _ in self.cards]:
                    continue

                for suit in suits:
                    card = Card(suit, rank)
                    if card not in self.cards:
                        self.target_cards.append(card)

            self.weights = [
                dict(
                    zip(
                        [card.as_tuple for card in self.target_cards],
                        [1 / 3 for _ in range(len(self.target_cards))]
                    )
                ) for _ in range(3) #3 opponents
            ]

        else:
            my_ranks = set([c.rank for c in self.cards])

            target_cards = [card for card in self.target_cards if card.rank in my_ranks]
            self.target_cards = target_cards


        # check game log to adjust weights
        
        self.update_weights(game)

        print(*self.weights)

        # select highest probability card
        max_p = -1
        selected_card = None
        for card, p in self.weights[target_id].items():
            if p > max_p:
                max_p = p
                selected_card = card

        # select target cards of same rank
        targets = [c for c in self.target_cards if c.rank == selected_card[0]]
        print(f"\tTARGETING {targets}")

        # generate a turn
        if len(targets) == 0:
            targets = [self.target_cards[0]]
            turn = self.targets_to_turn(targets)

        elif len(targets) == 3 or len(targets) == 1:
            turn = self.targets_to_turn(targets)

        else:
            targets = [Card(selected_card[1], selected_card[0])]
            turn = self.targets_to_turn(targets)
            
        return turn
        
        
        # get highest "weights"
            

