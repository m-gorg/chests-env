from Player import Player
from random import randint
from Turn import Turn
from Card import Card

ranks = [' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8']
suits = ['♠', '♥', '♣', '♦']

class PlayerProbabilistic(Player): # not susceptible to bluff
    
    def __init__(self, id):
        super().__init__(id)
        
        self.target_cards = None


    def targets_to_turn(self, targets):
        turn = Turn(targets[0][0].rank, len(targets), [t[0].suit for t in targets])
        return turn


    def rel_id(self, x):
        return (x - self.id - 1) % 4
    
    def set_weights(self, card, p):
        for i in range(3):
            self.weights[i][card.as_tuple] = p
    

    def update_weights(self, game):
        
        last_logs = []
        i = -1
        while True:
            try:
                last_logs.append(game.log[i])
            except:
                break
            i -= 1
            try:
                if game.log[i]['player'] == self.id:
                    last_logs.append(game.log[i])
                    break
            except:
                break
        
        # print(f"LOG COUNT: {len(last_logs)}")
        for log in last_logs: # 4 last logs for 3 oponents and us
            # print(log)
            player = self.rel_id(log['player'])
            target = self.rel_id(log['target'])

            if target == 3: # if we were targeted:
                pass #TODO

            match log['responce']:
                case 3: # guessed right
                    
                    for suit in log['turn'].suits:
                        card = Card(suit, log['turn'].rank)
                        if card in self.target_cards: # check if we care

                            self.set_weights(card, 0) # no one else has the card...
                            if player != 3:
                                self.weights[player][card.as_tuple] = 1 # except the one who guessed the card
                                self.amounts[player][card.rank] = [i + log['turn'].count for i in self.amounts[player][card.rank]]

                case 2: # wrong suit(s)

                    if target == 3:
                        continue
                    
                    if log['turn'].rank in set([c.rank for c in self.target_cards]):
                        self.amounts[target][log['turn'].rank] = [log['turn'].count] # set right amount

                    for suit in log['turn'].suits:
                        card = Card(suit, log['turn'].rank)
                        if card in self.target_cards:

                            for i in range(3):
                                if i == target:
                                    self.weights[i][card.as_tuple] /= 1.5 # lower W of having the suits
                                else:
                                    self.weights[i][card.as_tuple] *= 1.5
                    
                case 1: # wroung amount

                    # asking player has asked rank (unaccounted)
                    if target == 3: continue 

                    if log['turn'].rank in [card.rank for card in self.target_cards] and log['turn'].count in self.amounts[target][log['turn'].rank]: # do we care?
                        
                        self.amounts[target][log['turn'].rank].remove(log['turn'].count) # remove wrong amount from oponent's amount list

                    pass

                case 0: # no cards of given rank
                    
                    for suit in game.suits:
                        card = Card(suit, log['turn'].rank)
                        if card not in self.target_cards: # only cards we care about
                            continue
                        
                        #TODO? if len([c for c in self.target_cards if c.rank == log['turn'].rank]) == 1: # if we need only one card
                        
                        a, b = [i for i in range(3) if i != target]

                        wa, wb, wt = self.weights[a][card.as_tuple], self.weights[b][card.as_tuple], self.weights[target][card.as_tuple]
                        s = wa + wb
                        if s == 0:
                            continue
                        self.weights[a][card.as_tuple] += wt * wa / s
                        self.weights[b][card.as_tuple] += wt * wb / s
                        self.weights[target][card.as_tuple] = 0 # target has no cards of given rank

                        # for i in range(3):
                        #     if i == target:
                        #         self.weights[i][card.as_tuple] = 0 # target has no cards of given rank
                        #     else:
                        #         self.weights[i][card.as_tuple] += 1/6 # higher W that others have the card


    def get_turn(self, game, target_id):
        
        my_ranks = set([c.rank for c in self.cards])

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

            #  possible amounts of cards of a given rank
            self.amounts = [
                dict([                    
                    [rank, []] for rank in set(card.rank for card in self.target_cards) # target ranks
                ]) for _ in range(3) #3 opponents
            ]
            
            for i in range(3): # 3 oponents
                for rank in my_ranks:
                    self.amounts[i][rank] = [j + 1 for j in range(len([card for card in self.target_cards if card.rank == rank]))]

        else:

            target_cards = []
            for card in self.target_cards:
                if card.rank in my_ranks and card not in self.cards:
                    target_cards.append(card) # remove outdated targets...

                else:
                    for i in range(3):
                        self.weights[i][card.as_tuple] = 0 # and weights

            self.target_cards = target_cards

        # print("")
        # print(*self.weights)
        # print("")
        # print(*self.amounts)
        # print("")
        # check game log to adjust weights
        self.update_weights(game)


        # select highest probability card
        max_p = -1
        selected_card = None
        for card, p in self.weights[target_id].items():
            if p > max_p:
                max_p = p
                selected_card = card

        # select target cards of same rank
        targets = [[c, 0] for c in self.target_cards if c.rank == selected_card[0]] # store card, P for selected cards
        for t in targets:
            t[1] = self.weights[target_id][t[0].as_tuple]
        
        targets.sort(key = lambda x: x[1], reverse=True) # sort cards by higher P descending
        
        # print(f"TARGETING", *[t[0] for t in targets], *[t[1] for t in targets])

        # generate a turn
        if len(targets) == 0:
            targets = [[self.target_cards[0], 0]]
            turn = self.targets_to_turn(targets)

        elif len(targets) == 3 and 3 in self.amounts[target_id][targets[0][0].rank]:
            turn = self.targets_to_turn(targets)

        elif len(targets) == 1 or 1 in self.amounts[target_id][targets[0][0].rank]:
            turn = self.targets_to_turn(targets[:1])

        else: # == 1
            # targets = [Card(selected_card[1], selected_card[0])]
            turn = self.targets_to_turn(targets[:2])
            
        return turn
        
        
        # get highest "weights"
            

