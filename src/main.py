from games.GameNodeckRandom import GameNodeckRandom
from players.PlayerProbabilistic import PlayerProbabilistic
from players.PlayerRandom import PlayerRandom


players = [PlayerRandom(0),
           PlayerRandom(1),
           PlayerRandom(2),
           PlayerProbabilistic(3)]

game = GameNodeckRandom([' 2', ' 3', ' 4', ' 5', ' 6'],
            ['♠', '♥', '♣', '♦'],
            players,
            verbose=True)

game.start()

while True:
    if game.step():
        break

game.summary()

# for i in game.log:
#     print(i)
