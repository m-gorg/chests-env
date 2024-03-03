from games.GameDeckRandom import GameDeckRandom
from games.GameNodeckRandom import GameNodeckRandom
from players.PlayerRandom import PlayerRandom
from players.PlayerRandomNoReapeat import PlayerRandomNoRepeat


players = [PlayerRandom(i) for i in range(4)]

game = GameNodeckRandom([' 2', ' 3', ' 4', ' 5', ' 6'],
            ['♠', '♥', '♣', '♦'],
            players,
            verbose=True)

game.start()

while True:
    if game.step():
        break

for i in game.log:
    for j in i:
        print(j, end="  ")
    print("")
