from typing import List, Any

import pandas as pd
import matplotlib.pyplot as plt
from leagueDocs.agl.AGL import AGL
from leagueDocs.agl.analysis.ExpectedVsActualRecord import ExpectedVsActualRecord
from statistics import mean, median, mode, stdev

# the games that are legal and in the league
gameNames = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong', 'Darts',
             'Knockout', 'Pool', "Shuffleboard", "Word_Hunt", "Golf"]
# players in current season
playerNames = ["Dani", "Moshe", "Brick", "Ilan", "Hagler", "Goldstein", "Judah", "Ennis",
               "Alyssa", "Shmuli", "Ving", "Zach", "Siegel", "Elie"]

# players in previous season (season 2)
previous_season_players = ["Yitzie", "Benji", "Brick", "Ilan", "Hagler", "Goldstein", "Judah", "Ennis",
                           "Alyssa", "Shmuli", "Ving", "Zach", "Siegel", "Eli"]
previous_season_east = ['Brick', 'Hagler', "Benji", "Ilan", "Goldstein", "Judah", "Yitzie"]

agl = pd.read_csv('../schedules/AGL Season 3 - Schedule.csv')  # read schedule tab into a panda dataframe
agl = agl.drop(columns=['Games List', 'Comments', 'The Rulebook'])  # take out useless columns
agl = agl.dropna()   # get rid of any empty rows, this is needed for when we run the code mid season and there are
# games that have not been played

previous_season = pd.read_csv("../schedules/season_2_schedule.csv")     # read schedule tab into a panda dataframe
# the previous doc had less on the top row, just the game list must be stripped
previous_season = previous_season.drop(columns=['Games List', 'Comments'])
previous_season = previous_season.dropna()

# current season's east players
east = ['Brick', 'Ennis', "Alyssa", "Ilan", "Ving", "Judah", "Dani"]
# creat this season's AGL POPOs
league = AGL(player_names=playerNames, games=gameNames, schedule=agl,
             games_per_day=14, num_of_weeks=7, east=east, season_num=3)
previous_league = AGL(player_names=previous_season_players, games=gameNames,schedule=previous_season,
                      games_per_day=14, num_of_weeks=7, east=previous_season_east, season_num=2)


# Create the players stats CSV which will go on the doc
game_with_stats = ['Basketball', 'Cup Pong', 'Darts', 'Knockout', 'Pool', "Shuffleboard", "Golf"]
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

df2 = pd.DataFrame(AllGamesStats, columns=['Player', 'Ws', 'Ls', 'Win %', 'AVG',
                                           'Differential', 'AVG Win Differential', 'High Score',
                                           'Low Score', 'OTs'])
df2.to_csv('../produced_docs/Player Stats.csv')

# This will make the week's stats CSV which has essentially been replaced by the tab we currently have
# we can probably get rid of this
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
dfw.to_csv('../produced_docs/Week Stats.csv')

# Now we make all of the graphs

# p, opponent, and avg are all lists
# where in each of them, the element at index i = the person's, opponent's, and leage avg score for week i - 1
# and player is a string of the player name
# USE NEW COLORS from this link
# https://github.com/vega/vega/wiki/Scales#scale-range-literals
colors = {'#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
          '#aec7e8', '#ffbb78', '#98df8a', '#ff9896'}
# names, color = np.meshgrid(league.players, colors)
plt.plot(range(1, 70), label='games played')
plt.ylabel('Win Percentage')
plt.xlabel('Games played')
plt.title('Ranked Players by Win Percentage')
for name, color in zip(league.players, colors):
    plt.plot(league.players.get(name).list_of_win_percentage, label=name, color=color)
# for player in league.players:
#     plt.plot(league.players.get(player).list_of_win_percentage, label=player)

plt.legend()
plt.show()

plt.plot(range(1, 70), label='games played')
plt.xlabel('Games Won')
plt.xlabel('Games played')
plt.title('Ranked Players by Wins')
for name, color in zip(league.players, colors):
    plt.plot(league.players.get(name).list_of_wins, label=name, color=color)
plt.legend()
plt.show()

# plt.plot(range(1, 70), label='games played')
# plt.xlabel('Games Won')
# plt.xlabel('Games played')
# plt.title('Ranked Players by Losses')
# for name, color in zip(league.players, colors):
#     plt.plot(league.players.get(name).list_of_losses, label=name, color=color)
# plt.legend()
# plt.show()


plt.plot(range(1, 70), label='games played')
plt.ylabel('Win Percentage')
plt.xlabel('Games played')
plt.title('North Wing Players by Win Percentage')
for name, color in zip(league.players, colors):
    if east.__contains__(name):
        plt.plot(league.players.get(name).list_of_win_percentage, label=name, color=color)
plt.legend()
plt.show()

plt.plot(range(1, 70), label='games played')
plt.ylabel('Win Percentage')
plt.xlabel('Games played')
plt.title('South Wing Players by Win Percentage')
for name, color in zip(league.players, colors):
    if not east.__contains__(name):
        plt.plot(league.players.get(name).list_of_win_percentage, label=name, color=color)
# for player in league.players:
#     plt.plot(league.players.get(player).list_of_win_percentage, label=player)
plt.legend()
plt.show()

# plt.plot(range(1, 70), label='games played')
plt.xlabel('Rank')
plt.xlabel('Games played')
plt.title('Players by Rank')
for name, color in zip(league.players, colors):
    dict_percentages = league.players.get(name).dict_of_win_percent
    for game_num in dict_percentages.keys():
        my_percentage = dict_percentages.get(game_num)
        rank = 1
        for player_name in league.players:
            opponent_percentage = league.players.get(player_name).dict_of_win_percent.get(game_num)
            if opponent_percentage is None:
                continue
            if opponent_percentage > my_percentage:
                rank += 1
        league.players.get(name).rank[game_num] = rank
    rank_list = list(league.players.get(name).rank.values())
    plt.plot(rank_list, label=name, color=color)
plt.legend()
plt.show()

plt.xlabel('Rank')
plt.xlabel('Games played')
plt.title('South Wing Players by Rank')
for name, color in zip(league.players, colors):
    if not east.__contains__(name):
        dict_percentages = league.players.get(name).dict_of_win_percent
        for game_num in dict_percentages.keys():
            my_percentage = dict_percentages.get(game_num)
            rank = 1
            for player_name in league.players:
                if not east.__contains__(player_name):
                    opponent_percentage = league.players.get(player_name).dict_of_win_percent.get(game_num)
                    if opponent_percentage is None:
                        continue
                    if opponent_percentage > my_percentage:
                        rank += 1
            league.players.get(name).rank[game_num] = rank
        rank_list = list(league.players.get(name).rank.values())
        plt.plot(rank_list, label=name, color=color)
plt.legend()
plt.show()

plt.xlabel('Rank')
plt.xlabel('Games played')
plt.title('North Wing Players by Rank')
for name, color in zip(league.players, colors):
    if east.__contains__(name):
        dict_percentages = league.players.get(name).dict_of_win_percent
        for game_num in dict_percentages.keys():
            my_percentage = dict_percentages.get(game_num)
            rank = 1
            for player_name in league.players:
                if east.__contains__(player_name):
                    opponent_percentage = league.players.get(player_name).dict_of_win_percent.get(game_num)
                    if opponent_percentage is None:
                        continue
                    if opponent_percentage > my_percentage:
                        rank += 1
            league.players.get(name).rank[game_num] = rank
        rank_list = list(league.players.get(name).rank.values())
        plt.plot(rank_list, label=name, color=color)
plt.legend()
plt.show()

# objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
# players = league.players
# avg = []
# for name in players:
#     avg.append(league.players.get(name).stats.get("Basketball").avg_score)
# y_pos = np.arange(len(players))
# performance = [10,8,6,4,2,1]
#
# plt.bar(y_pos, avg, align='center', alpha=0.5)
# plt.xticks(y_pos, league.players.get(name))
# plt.ylabel('Usage')
# plt.title('Programming language usage')
#
# plt.show()

#
# print("Basketball stats")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).stats['Basketball']))
#
# print()
# print("Shuffleboard stats")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).stats['Shuffleboard']))
#
# print()
# print("Pool stats")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).stats['Pool']))
#
# print()
# print("Darts stats")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).stats['Darts']))
#
# print()
# print("Cup Pong stats")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).stats['Cup Pong']))
#
#
# print()
# print("Last 10")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).count_record_for_last_n(10)))
#
# print()
# print("Last 20")
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).count_record_for_last_n(20)))
#
# for player in league.players:
#     print(player + ",  " + str(league.players.get(player).print_division_record()))


expected_record = ExpectedVsActualRecord(league)
expected_record.calculate_results()

print()
print("####################################################################")
print()
print("Season 2 expected VS actual")
last_season_expected = ExpectedVsActualRecord(previous_league)
last_season_expected.calculate_results()
#
print()
print("####################################################################")
print()
# + " mode: " + str(mode(game_data))
print(AGL.data_collector.get_all_avgs())
for game in AGL.data_collector.game_scores.keys():
    game_data: List[Any] = AGL.data_collector.get_all_scores_for_a_game(game)
    if len(game_data) > 0:
        print(game + ":  mean: " + str(mean(game_data)) + " median: " + str(median(game_data))
              + " std: " + str(stdev(game_data))
              + " number of datapoints: " + str(len(game_data)))

print("done")

# print()
# print()
# print()
# print("######### PRINT EVERYTHING ############")
# for player in league.players:
#     print()
#     print()
#     print(player + ":")
#     print(league.players.get(player).print())
#
#
# print()
# print()
# print()
# print("######### PRINT Division Records ############")
# for player in league.players:
#     print()
#     print(player + ":")
#     print(league.players.get(player).print_division_record())



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
