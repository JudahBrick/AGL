import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from leagueDocs import Player, StatsPerGame


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
            wins = 0
            losses = 0
            unexpected = []

            for match_up in name_player.games:
                match = match_up.split("&")
                game_name = match[0]
                opponent_name = match[1]
                actually_won = (match[2] == 'True')
                score = match[3]
                should_win, win_perc_chance = self.should_player_a_win(name, game_name, opponent_name)
                # print(name + " against " + opponent_name + " in " + game_name +
                #       ". win % chance: " + str(win_perc_chance))
                if should_win:
                    wins += 1
                else:
                    losses += 1

                string = ""
                # print("should win: " + str(should_win) + "  actual: " + str(actually_won))
                # if there was an unexpected winner, then log it
                if should_win is True and actually_won is False:
                    string += "Lost in "
                elif should_win is False and actually_won is True:
                    string += "Won in "
                # if there was an unexpected winner, then log it
                if not string == "":
                    string += game_name + " against " + opponent_name + " Score: " + score \
                              + " win% chance: " + str(win_perc_chance)
                    unexpected.append(string)
                    # print("should win: " + str(should_win) + "  actual: " + str(actually_won)+ "  String: " + string)

            # print out all of the player's expected vs actual records, along with the unexpected game wins/losses
            print(name + "'s expected record: " + str(wins) + "-" + str(losses) + "   Actual: "
                  + str(name_player.total_wins) + "-" + str(name_player.total_losses))
            print("Unexpected wins/losses:")
            print(unexpected)
            print()


    def should_player_a_win(self, player_a: str, game: str, opponent_name):
        # TODO finish this method so we can do schedule difficulty
        #  1) this should check to see if this game is a game we should go based off of an average like basketball
        #  2) if it isn't a game like that then it should just be based off
        #     of the record of that player in that specific game
        # , "Darts", "Pool", "Shuffleboard", "Cup Pong"
        scored_games = ["Basketball"]

        stats_game = league.players.get(player_a).get_stats()
        player_a_stats = stats_game[game]
        stats_game = league.players.get(opponent_name).get_stats()
        opponent_stats = stats_game[game]
        win_perc_chance = self.win_percent_likelyhood_for_a(player_a_stats, opponent_stats)
        if scored_games.__contains__(game):
            return self.should_player_a_win_scored_game(player_a_stats, opponent_stats), win_perc_chance
        else:
            return self.should_player_a_win_not_scored_game(player_a_stats, opponent_stats), win_perc_chance

    def should_player_a_win_scored_game(self, player_a: StatsPerGame, opponent: StatsPerGame):
        # check avg score
        if player_a.avg_score > opponent.avg_score:
            return True
        elif player_a.avg_score < opponent.avg_score:
            return False
        # then check win percentage
        elif player_a.win_percentage > opponent.win_percentage:
            return True
        elif player_a.win_percentage < opponent.win_percentage:
            return False
        # then check highest score
        elif player_a.high_score > opponent.high_score:
            return True
        elif player_a.high_score < opponent.high_score:
            return False
        # then check lowest score
        elif player_a.lowest_score < opponent.lowest_score:
            return True
        elif player_a.lowest_score > opponent.lowest_score:
            return False

    def should_player_a_win_not_scored_game(self, player_a: StatsPerGame, opponent: StatsPerGame):
        if player_a.win_percentage > opponent.win_percentage:
            return True
        elif player_a.win_percentage < opponent.win_percentage:
            return False
        elif player_a.high_score > opponent.high_score:
            return True
        elif player_a.high_score < opponent.high_score:
            return False
        elif player_a.lowest_score < opponent.lowest_score:
            return True
        elif player_a.lowest_score > opponent.lowest_score:
            return False


    def win_percent_likelyhood_for_a(self, player_a: StatsPerGame, opponent: StatsPerGame):
        # XWins = my-win-percentage / (my-win-percentage + opponents-win-percentage)
        a_wins = player_a.wins + .5
        a_losses = player_a.losses + .5
        a_win_perc = win_percentage(a_wins, a_losses)

        o_wins = opponent.wins + .5
        o_losses = opponent.losses + .5
        o_win_perc = win_percentage(o_wins, o_losses)
        a_wins_this_game = round((a_win_perc / (a_win_perc + o_win_perc)) * 100, 1)
        return a_wins_this_game


def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)


gameNames = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong', 'Darts',
             'Knockout', 'Pool', "Shuffleboard", "Word_Hunt", "Golf"]
playerNames = ["Dani", "Moshe", "Brick", "Ilan", "Hagler", "Goldstein", "Judah", "Ennis",
               "Alyssa", "Shmuli", "Ving", "Zach", "Siegel", "Eli"]

agl = pd.read_csv('AGL Season 3 - Schedule.csv')
difficulty = pd.read_csv('AGL Season 3 - Schedule.csv')

agl = agl.drop(columns=['Games List', 'Comments', 'The Rulebook'])
agl = agl.dropna()
difficulty = difficulty.drop(columns=['Games List', 'Comments', 'The Rulebook'])
difficulty = difficulty.dropna()

# print(agl.head(20))

# print(agl[0:20])
# agl['game_num'] = agl.

# agl['game_number'] = range(1, 1 +len(agl))
# agl.set_index('game_number')
# print(agl.head(5))
# print(agl.columns)
east = ['Brick', 'Ennis', "Alyssa", "Ilan", "Ving", "Judah", "Dani"]
league = AGL(player_names=playerNames, games=gameNames, schedule=agl, games_per_day=14, num_of_weeks=7, east=east)
for player in league.players:
    league.players.get(player).print_per_week_win_ration()

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


league.schedule_difficulty()
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
