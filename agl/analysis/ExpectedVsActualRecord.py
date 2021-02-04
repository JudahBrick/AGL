from typing import Tuple, Union, Any

from leagueDocs.agl import AGL
from leagueDocs.agl import StatsPerGame

import pandas as pd

class ExpectedVsActualRecord:
    def __init__(self, season: AGL):
        self.season = season

    def calculate_results(self) -> None:
        upsets = []

        for name in self.season.players:
            name_player = self.season.players.get(name)
            wins = 0
            losses = 0
            unexpected_wins = 0
            unexpected_losses = 0
            unexpected = []

            for match_up in name_player.games:
                match = match_up.split("&&")
                game_name = match[0]
                opponent_name = match[1]
                actually_won = (match[2] == 'True')
                score = match[3]
                # print(name + " against " + opponent_name + " in " + game_name)
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
                    unexpected_losses += 1
                elif should_win is False and actually_won is True:
                    string += "Won in "
                    unexpected_wins += 1
                    # this is for a csv to upload,
                    # we will only log the winning games and not both

                    # get the wins-losses for oth players in this game
                    stats_game = self.season.players.get(name).get_stats()
                    winner = stats_game[game_name]
                    winner = '(' + winner.get_win_loss_string() + ')'
                    stats_game = self.season.players.get(opponent_name).get_stats()
                    loser = stats_game[game_name]
                    loser = '(' + loser.get_win_loss_string() + ')'
                    # add it to the df so it can go to csv later
                    upsets.append([name, winner, game_name, opponent_name,
                                   loser, score, win_perc_chance])
                # if there was an unexpected winner, then log it
                if not string == "":
                    string += game_name + " against " + opponent_name + " Score: " + score \
                              + " win% chance: " + str(win_perc_chance)
                    unexpected.append(string)
                    # print("should win: " + str(should_win) + "  actual: " + str(actually_won)+ "  String: " + string)

            # print out all of the player's expected vs actual records, along with the unexpected game wins/losses
            print(name + "'s expected record: " + str(wins) + "-" + str(losses) + "   Actual: "
                  + str(name_player.total_wins) + "-" + str(name_player.total_losses) + "  unexpected wins-losses: "
                  + str(unexpected_wins) + "-" + str(unexpected_losses))
            print("Unexpected wins/losses:")
            print(unexpected)
            print()

            dfw = pd.DataFrame(upsets, columns=['Winner', 'Winner record in game', 'Game', 'Loser',
                                                'Loser record in game', 'Score', 'Win % Chance'])
            dfw.to_csv('../produced_docs/Upsets Season ' + str(self.season.season_num) + '.csv')

    def should_player_a_win(self, player_a: str, game: str, opponent_name) -> Tuple[bool, Union[float, Any]]:
        # TODO finish this method so we can do schedule difficulty
        #  1) this should check to see if this game is a game we should go based off of an average like basketball
        #  2) if it isn't a game like that then it should just be based off
        #     of the record of that player in that specific game
        # , 'Cup Pong', 'Darts', 'Pool', 'Anagrams', "Word_Hunt"
        scored_games = ["Basketball", "Golf", 'Shuffleboard', 'Cup Pong', 'Darts', 'Pool', 'Anagrams', "Word_Hunt"]

        stats_game = self.season.players.get(player_a).get_stats()
        player_a_stats = stats_game[game]
        stats_game = self.season.players.get(opponent_name).get_stats()
        opponent_stats = stats_game[game]
        win_perc_chance = win_percent_likelyhood_for_a(player_a_stats, opponent_stats)


        if scored_games.__contains__(game):
            return should_player_a_win_scored_game(player_a_stats, opponent_stats), win_perc_chance
        else:
            return should_player_a_win_not_scored_game(player_a_stats, opponent_stats), win_perc_chance

    def game_rankings_for_players(self, season_players=[]):

        scored_games = ["Basketball", "Golf", 'Shuffleboard', 'Cup Pong', 'Darts', 'Pool', 'Anagrams', "Word_Hunt"]
        if len(season_players) is 0:
            season_players = self.season.players


        rankings_by_game_wins = {}
        rankings_by_game_avg_score = {}
        rankings_by_game_by_win = {}
        rankings_by_game_by_score = {}
        dfs_of_games = {}
        for game in self.season.games:
            list_to_become_df = []


            # print()
            # print(game)
            rankings_by_wins = {}
            rankings_by_avg_score = {}
            combined_rankings = []

            for player_a in season_players:
                rank_by_wins: int = 0
                rank_by_avg_score: int = 0
                # combined_rank: float = 0
                for player_b in season_players:

                    stats_game = self.season.players.get(player_a).get_stats()
                    player_a_stats = stats_game[game]
                    stats_game = self.season.players.get(player_b).get_stats()
                    opponent_stats = stats_game[game]

                    if not should_player_a_win_not_scored_game(player_a_stats, opponent_stats):
                        rank_by_wins += 1
                        if game == 'Knockout' or game == 'Archery':
                            rank_by_avg_score += 1

                    if scored_games.__contains__(game):
                        if not should_player_a_win_scored_game(player_a_stats, opponent_stats):
                            rank_by_avg_score += 1


                # rankings_by_wins.append((rank_by_wins, player_a))
                rankings_by_wins[player_a] = rank_by_wins
                # rankings_by_avg_score.append((rank_by_avg_score, player_a))
                rankings_by_avg_score[player_a] = rank_by_avg_score
                avg_rank: float = (rank_by_wins + rank_by_avg_score) / 2
                combined_rankings.append((avg_rank, player_a))

                # rankings.append([player_a, rank_by_wins, rank_by_avg_score, avg_rank])
                list_to_become_df.append([player_a, rank_by_wins, rank_by_avg_score, avg_rank])

            rankings_by_wins = sorted(rankings_by_wins)
            rankings_by_avg_score = sorted(rankings_by_avg_score)
            combined_rankings = sorted(combined_rankings)
            rankings_by_game_by_win[game] = rankings_by_wins
            rankings_by_game_by_score[game] = rankings_by_avg_score

            df_of_game_rankings = pd.DataFrame(list_to_become_df,
                                               columns=['player', 'rank by wins', 'rank by score', 'combined ranks'])
            df_of_game_rankings.sort_values("player", inplace=True)

            # creating a rank column and passing the returned rank series
            # change method to 'min' to rank by minimum
            df_of_game_rankings["rank"] = df_of_game_rankings["combined ranks"].rank(method='min')
            # rankings.append(df_of_game_rankings)
            dfs_of_games[game] = df_of_game_rankings

        dfs_of_players = {}
        for player in season_players:
            dfs_of_players[player] = []

        rankings = []
        for game in dfs_of_games:
            df = dfs_of_games[game]

            for index, row in df.iterrows():
                rankings.append(
                    [game, row['player'], row['rank by wins'],
                     row['rank by score'], row['combined ranks'], row['rank']])
                dfs_of_players[row['player']].append([game, row['rank']])

        df2 = pd.DataFrame(rankings,
                           columns=['Game', 'player', 'rank by wins', 'rank by score', 'combined ranks', 'rank'])
        df2.to_csv('../produced_docs/ranks for season.csv')

        preferences = []
        for player in dfs_of_players:
            game_ranks = dfs_of_players[player]
            df = pd.DataFrame(game_ranks, columns=['game', 'rank'])
            df["preference"] = df["rank"].rank(method='min')
            for index, row in df.iterrows():
                preferences.append([player, row['game'], row['rank'], row['preference']])

        preferences_df = pd.DataFrame(preferences, columns=['player', 'game', 'rank', 'preferences'])
        preferences_df.to_csv('../produced_docs/preferences for season.csv')

def should_player_a_win_not_scored_game(player_a: StatsPerGame, opponent: StatsPerGame):
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


def should_player_a_win_scored_game(player_a: StatsPerGame, opponent: StatsPerGame):
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


def win_percent_likelyhood_for_a(player_a: StatsPerGame, opponent: StatsPerGame):
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

