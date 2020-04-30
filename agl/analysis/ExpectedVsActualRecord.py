from typing import Tuple, Union, Any

from leagueDocs.agl import AGL
from leagueDocs.agl import StatsPerGame

class ExpectedVsActualRecord:
    def __init__(self, season: AGL):
        self.season = season

    def calculate_results(self) -> None:
        for name in self.season.players:
            name_player = self.season.players.get(name)
            wins = 0
            losses = 0
            unexpected_wins = 0
            unexpected_losses = 0
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
                    unexpected_losses += 1
                elif should_win is False and actually_won is True:
                    string += "Won in "
                    unexpected_wins += 1
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

    def should_player_a_win(self, player_a: str, game: str, opponent_name) -> Tuple[bool, Union[float, Any]]:
        # TODO finish this method so we can do schedule difficulty
        #  1) this should check to see if this game is a game we should go based off of an average like basketball
        #  2) if it isn't a game like that then it should just be based off
        #     of the record of that player in that specific game
        # , "Darts", "Pool", "Shuffleboard", "Cup Pong"
        scored_games = ["Basketball"]

        stats_game = self.season.players.get(player_a).get_stats()
        player_a_stats = stats_game[game]
        stats_game = self.season.players.get(opponent_name).get_stats()
        opponent_stats = stats_game[game]
        win_perc_chance = win_percent_likelyhood_for_a(player_a_stats, opponent_stats)
        if scored_games.__contains__(game):
            return should_player_a_win_scored_game(player_a_stats, opponent_stats), win_perc_chance
        else:
            return should_player_a_win_not_scored_game(player_a_stats, opponent_stats), win_perc_chance


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

