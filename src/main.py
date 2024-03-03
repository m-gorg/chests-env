from games.GameDeckRandom import GameDeckRandom
from games.GameNodeckRandom import GameNodeckRandom
from players.PlayerRandom import PlayerRandom
from players.PlayerRandomNoReapeat import PlayerRandomNoRepeat


players = [PlayerRandom(i) for i in range(4)]

game = GameNodeckRandom([' 2', ' 3', ' 4', ' 5', ' 6'],
            ['♠', '♥', '♣', '♦'],
            players,
            verbose=False)

game.start()

while True:
    if game.step():
        break