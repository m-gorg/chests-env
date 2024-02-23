from games.GameDeckRandom import GameDeckRandom
from players.PlayerRandom import PlayerRandom

players = [PlayerRandom(i) for i in range(4)]

game = GameDeckRandom([' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9'],
            ['♠', '♥', '♣', '♦'],
            players)

game.start()

while True:
    if game.step():
        break