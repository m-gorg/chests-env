from Game import Game
from Player import Player
from random import randint, choice

# Game variant with all cards allready drawn
# 4+ players advised

class GameNodeckRandom(Game):
    
    def __init__(self, ranks, suits, players, verbose=False):
        super().__init__(ranks, suits, players, verbose)

    def start(self):
        self.log = []
        self.current_player_id = 0

        for player in self._players:
            for _ in range(int(len(self.ranks) * len(self.suits) / len(self._players))):
                player.add_card(self._deck.draw())
            
            self.check_for_chests(player)
            self._starting_state[player.id] = [_ for _ in player.cards]

    
    def step(self, turn=None):
        current_player = self._players[self.current_player_id]

        # get random target
        while True:

            if self.responce != 3:
                self.rel_target_id = randint(0, len(self._players) - 2)
            else:
                self.rel_target_id = self.next_target(self.rel_target_id)

            target_id = (self.current_player_id + self.rel_target_id + 1) % len(self._players)

            if not self.out[target_id]:
                break
    
        target = self._players[target_id]

        if turn == None:
            turn = current_player.get_turn(self, self.rel_target_id)

        # turn validation
        valid = False
        for card in current_player.cards:
            if card.rank == turn.rank:
                valid = True
                break
        
        if not valid:
            raise Exception("Invalid turn")
        
        if self.verbose:
            print(f"{current_player.id} -> {target.id}: {turn}")
        # get responce from turn
        self.responce = self.turn_responce(turn, target)


        # trasfer cards and log
        mask_turn = turn
        match self.responce:
            case 3: # guessed right
                self.transfer_cards(current_player, target, turn)
            case 2: # wrong suit(s)
                pass
            case 1: # wroung amount
                mask_turn.suits = None
            case 0: # no cards of given rank
                mask_turn.suits = None
                mask_turn.count = None


        self.log.append({'player': self.current_player_id, 
                         'target': target.id,
                         'turn': mask_turn, 
                         'responce': self.responce})
        

        self.check_for_chests(current_player)

        # select players that are leaving the game
        for i, player in enumerate(self._players):
            if len(player.cards) == 0 and self._deck.size == 0:
                self.out[i] = True

        
                if self.current_player_id == i and self.out.count(True) <= 2:
                    self.current_player_id = self.next_player_id(self.current_player_id)

         # check for end of game 
        if self.out.count(True) > 2:
            return True

        if self.verbose:
            for player in self._players:
                print(f"\nPlayer {player.id}:")
                for card in player.cards:
                    print(card, end=" ")
            print("")

        if self.responce != 3:
            self.current_player_id = self.next_player_id(self.current_player_id)

        return False
