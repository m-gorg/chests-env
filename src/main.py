from games.GameNodeckRandom import GameNodeckRandom
from players.PlayerProbabilistic import PlayerProbabilistic
from players.PlayerRandom import PlayerRandom

import numpy as np
from matplotlib import pyplot as plt


def init():
    players = [PlayerRandom(0),
               PlayerRandom(1),
               PlayerRandom(2),
               PlayerRandom(3)]

    game = GameNodeckRandom([' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8'],
            ['♠', '♥', '♣', '♦'],
            players,
            verbose=True)
    
    return players, game


games = []
n = 1

if __name__ == "__main__":

    for i in range(n): # simulate n games

        players, game = init()

        game.start()

        while True:
            if game.step():
                break

        summary = game.summary()

        # for player, cards in summary['chests'].items():
        #     print(f"Player {player} - {int(len(cards) / 4)} chests")

        games.append({'log': game.log, 'summary': summary})

    lengths = []
    # win_stats = dict([[p.id, 0] for p in players])
    chests_stats = dict([[p.id, []] for p in players])
    delta_cards_stats = dict([[p.id, []] for p in players])

    for game in games:
        lengths.append(len(game['log']))

        # max_chests = 
        for i in [p.id for p in players]:
            chests_stats[i].append(int(len(game['summary']['chests'][i]) / 4))
            delta_cards_stats[i].append(int(len(game['summary']['chests'][i])) - len([p.rank for p in game['summary']['start'][i]]))

    print(np.mean(lengths))
    # print(chests_stats)
    # print(delta_cards_stats)
    
    # print(delta_cards_stats.values())
    plt.hist(delta_cards_stats[0])

    plt.show()
