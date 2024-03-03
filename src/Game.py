from Deck import Deck
from Card import Card

class Game:
    def __init__(self, ranks, suits, players, verbose):
        self.verbose = verbose

        self._deck = Deck(ranks, suits)

        self._players = players
        self.players_num = len(players)
        self.out = [False for _ in range(len(players))]

        self.ranks = ranks
        self.suits = suits
        
        for p in players:
            p.ranks = ranks
            p.suits = suits

        self.responce = None


    def check_for_chests(self, player):
        # could optimize with dictionaries or binary representation
        for rank in player.ranks:
            c = [card for card in player.cards if card.rank == rank]
            if len(c) == 4:
                for card in c:
                    player.cards.remove(card)
                    player.chests.append(card)

        # if len(player.cards) == 0:
        #     player.add_card(self._deck.draw())


    def next_player_id(self, player_id):
        id = (player_id + 1) % len(self._players)
        if not self.out[id] and self.current_player_id != id:
            return id
        else:
            return self.next_player_id(id)
        

    def next_target(self, target_id):
        id = (target_id + 1) % (len(self._players) - 1)
        return id


    def start(self):
        raise Exception(NotImplementedError)


    def transfer_cards(self, player, target, turn):
        for suit in turn.suits:
            card = Card(suit, turn.rank)
            
            target.remove_card(card)
            player.add_card(card)


    def turn_responce(self, turn, target):

        if turn.rank not in [card.rank for card in target.cards]:
            return 0

        relevant_cards_suits = [card.suit for card in target.cards if card.rank == turn.rank]
        count = len(relevant_cards_suits)

        if turn.count != count:
            return 1
        
        for suit in turn.suits:
            if suit not in relevant_cards_suits:
                return 2
        
        return 3
    

    def step(self):
        raise Exception(NotImplementedError)
