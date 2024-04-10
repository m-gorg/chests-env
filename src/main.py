from games.GameNodeckRandom import GameNodeckRandom
from players.PlayerProbabilistic import PlayerProbabilistic
from players.PlayerRandom import PlayerRandom

import numpy as np
from matplotlib import pyplot as plt


def init():
    players = [PlayerProbabilistic(0),
               PlayerProbabilistic(1),
               PlayerProbabilistic(2),
               PlayerProbabilistic(3)]

    game = GameNodeckRandom([' 2', ' 3', ' 4', ' 5', ' 6'],
            ['♠', '♥', '♣', '♦'],
            players,
            verbose=False)
    
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
    win_stats = dict([[p.id, 0] for p in players])
    chests_stats = dict([[p.id, 0] for p in players])
    delta_cards_stats = dict([[p.id, 0] for p in players])

    for game in games:
        lengths.append(len(game['log']))

        max_chests = -1
        best_id = 0

        for i in [p.id for p in players]:
            c = int(len(game['summary']['chests'][i]) / 4)
            chests_stats[i] += c
            delta_cards_stats[i] += int(len(game['summary']['chests'][i])) - len([p.rank for p in game['summary']['start'][i]])

            if c > max_chests:
                max_chests = c
                best_id = i

        win_stats[best_id] += 1

    print(np.mean(lengths))
    print(win_stats)
    # print(chests_stats)
    # print(delta_cards_stats)
    
    # print(delta_cards_stats.values())
    # plt.hist(delta_cards_stats[0])

    # plt.show()
