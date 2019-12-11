import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from leagueDocs import Player


class AGL:
    def __init__(self, player_names: [], schedule: pd.DataFrame, games: [], num_of_weeks: int,
                 games_per_day: int, east: []):
        self.players = {}
        for name in player_names:
            self.players[name] = Player.Player(name=name, games=games, num_of_weeks=num_of_weeks,
                                               player_names=player_names, east_division=name in east)
        self.schedule = schedule
        self.num_of_weeks = num_of_weeks
        self.games_per_day = games_per_day
        self.count()
        for player in self.players:
            self.players.get(player).count_win_percentages()

    def count(self):
        # game_number = 0
        # week_num = 1
        # game_per_week = self.games_per_day * 5
        for index, row in self.schedule.iterrows():
            home = row['Home']  # add home wins and losses
            away = row['Away']
            game = row['Game']
            winner = row['Winner']
            loser = row['Loser']
            score = row['Score']
            week_num = row['Week']

            if game == "Word Hunt":
                game = "Word_Hunt"
            if winner == loser:
                print("##########   loser == winner?!  ########")
                print(game + " " + winner + " " + loser + "     Score: " + score)
            self.players.get(winner).add_game_result(game=game, opponent=loser, won=True, home=home == winner,
                                                     opp_in_eastern_division=self.players.get(loser).east_division,
                                                     score=score)
            self.players.get(loser).add_game_result(game=game, opponent=winner, won=False, home=home == loser,
                                                    opp_in_eastern_division=self.players.get(winner).east_division,
                                                    score=score)
            # print('Week Num: ' + week_num)
            self.players.get(winner).week_stats.get(int(week_num)).add_game(game=game, win=True)
            self.players.get(loser).week_stats.get(int(week_num)).add_game(game=game, win=False)
            # print('Game Number: ' + str(game_number) + '  Week Number: ' + str(week_num))
            # game_number += 1
            # if game_number % game_per_week == 0:
            #     week_num += 1

    def schedule_difficulty(self):
        for name in self.players:
            name_player = self.players.get(name)
            east = name_player.east_division
            opponent_wins = 0
            opponent_losses = 0
            for opponent in self.players:
                if name == opponent:
                    continue
                opponent_player = self.players.get(opponent)
                if opponent_player.east_division == east:
                    opponent_wins += opponent_player.total_wins * 2
                    opponent_losses += opponent_player.total_losses * 2
                else:
                    opponent_wins += opponent_player.total_wins
                    opponent_losses += opponent_player.total_losses
            print(name + "'s opponent win percentage: " + str(win_percentage(opponent_wins, opponent_losses)))


def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)


gameNames = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong', 'Darts', 'Knockout', 'Pool', "Shuffleboard", "Word_Hunt"]
playerNames = ["Benji", "Yitzie", "Brick", "Ilan", "Hagler", "Goldstein", "Judah", "Ennis",
               "Alyssa", "Shmuli", "Ving", "Zach", "Siegel", "Eli"]


agl = pd.read_csv('season_2_schedule.csv')

agl = agl.drop(columns=['Games List', 'Comments'])
agl = agl.dropna()
print(agl.head(20))

#print(agl[0:20])
# agl['game_num'] = agl.

# agl['game_number'] = range(1, 1 +len(agl))
# agl.set_index('game_number')
print(agl.head(5))
print(agl.columns)
east = ['Brick', 'Yitzie', "Benji", "Ilan", "Hagler", "Judah", "Goldstein"]
league = AGL(player_names=playerNames, games=gameNames, schedule=agl, games_per_day=14, num_of_weeks=7, east=east)
for player in league.players:
    league.players.get(player).print_per_week_win_ration()

game_with_stats = ['Basketball', 'Cup Pong', 'Darts', 'Knockout', 'Pool', "Shuffleboard"]

AllGamesStats = []
for game in game_with_stats:
    AllGamesStats.append(['', '', '', '', '', game, '', '', ''])
    for player in league.players:
        stats_of_game = league.players.get(player).get_stats()
        player_stats = stats_of_game[game]

        AllGamesStats.append([player, player_stats.wins, player_stats.losses, player_stats.win_percentage,
                              player_stats.avg_score, player_stats.total_differential,
                              player_stats.avg_win_differential, player_stats.high_score,
                              player_stats.lowest_score, player_stats.total_ots])

df2 = pd.DataFrame(AllGamesStats, columns=['Player', 'Wins', 'Losses', 'Win Percentage', 'AVG Score',
                                           'Differential Score', 'AVG Win Differential Score', 'High Score',
                                           'Low Score', 'OTs'])
df2.to_csv('Player Stats.csv')

weeks_stats = []
for player in league.players:
    player_week_stats = league.players.get(player).week_stats
    weeks_stats.append([player, player_week_stats.get(1).just_win_loss_ratio(),
                        player_week_stats.get(2).just_win_loss_ratio(),
                        player_week_stats.get(3).just_win_loss_ratio(),
                        player_week_stats.get(4).just_win_loss_ratio(),
                        player_week_stats.get(5).just_win_loss_ratio(),
                        player_week_stats.get(6).just_win_loss_ratio(),
                        player_week_stats.get(7).just_win_loss_ratio(),
                        ])

dfw = pd.DataFrame(weeks_stats, columns=['Player', '1', '2', '3', '4', '5', '6', '7'])
dfw.to_csv('Week Stats.csv')

# p, opponent, and avg are all lists
# where in each of them, the element at index i = the person's, opponent's, and leage avg score for week i - 1
# and player is a string of the player name
colors = {'#070707', '#FF9F33', '#12F0D5', '#389DB4', '#FFF333',
          '#A5FF33', '#3AA439', '#0E4BEE', '#ABA2D6', '#9E6740',
          '#7C13B9', '#F60AD6', '#A77407', '#FB0417'}
# names, color = np.meshgrid(league.players, colors)
plt.plot(range(1, 70), label='games played')
plt.ylabel('Win Percentage')
plt.xlabel('Games played')
plt.title('Ranked PLayers by Win Percentage')
for name, color in zip(league.players, colors):
    plt.plot(league.players.get(name).list_of_win_percentage, label=name, color=color)
# for player in league.players:
#     plt.plot(league.players.get(player).list_of_win_percentage, label=player)

plt.legend()
plt.show()

plt.plot(range(1, 70), label='games played')
plt.xlabel('Games Won')
plt.xlabel('Games played')
plt.title('Ranked PLayers by Wins')

for name, color in  zip(league.players, colors):
    plt.plot(league.players.get(name).list_of_wins, label=name, color=color)

plt.legend()
plt.show()

plt.plot(range(1, 70), label='games played')
plt.xlabel('Games Won')
plt.xlabel('Games played')
plt.title('Ranked PLayers by Losses')

for name, color in zip(league.players, colors):
    plt.plot(league.players.get(name).list_of_losses, label=name, color=color)

plt.legend()
plt.show()




print("Basketball stats")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).stats['Basketball']))

print()
print("Shuffleboard stats")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).stats['Shuffleboard']))

print()
print("Pool stats")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).stats['Pool']))

print()
print("Darts stats")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).stats['Darts']))

print()
print("Cup Pong stats")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).stats['Cup Pong']))


print()
print("Last 10")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).count_record_for_last_n(10)))

print()
print("Last 20")
for player in league.players:
    print(player + ",  " + str(league.players.get(player).count_record_for_last_n(20)))

for player in league.players:
    print(player + ",  " + str(league.players.get(player).print_division_record()))




# league.schedule_difficulty()
#
# print()
# print()
# print()
# print("######### PRINT EVERYTHING ############")
# for player in league.players:
#     print()
#     print()
#     print(player + ":")
#     print(league.players.get(player).print())

# players = {}
#
#
# for name in playerNames:
#     players[name] = Player.Player(name=name, games=gameNames, player_names=playerNames, num_of_weeks=weeks)
#
#
# for player in players:
#     print()
#     print()
#     players[player].print()
#
# for player in player:
#     players[player].week_stats.get(1)

#
# print()
# print()
# print()
# print()
# print("######    iterating  ######")
# # row = next(agl.iteritems())
# agl = agl.tail(10)
#
#
# for index, row in agl.iterrows():
#     home = row['Home']
#     away = row['Away']
#     game = row ['Game']
#     winner = row['Winner']
#     loser = row['Loser']
#     print(winner + " beat " + loser + " in " + game)
#
# agl = agl.tail(10)

