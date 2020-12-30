from leagueDocs.agl import AGL
import pandas as pd


class SeasonStatsPrinter:

    def __init__(self, league: AGL,  games_with_stats: [], season_name: str):
        self.league = league
        self.games_with_stats = games_with_stats
        self.season_name = season_name

    def print(self):
        all_games_stats = []
        for game in self.games_with_stats:
            all_games_stats.append(['', '', '', '', '', game, '', '', ''])
            for player in self.league.players:
                stats_of_game = self.league.players.get(player).get_stats()
                player_stats = stats_of_game[game]

                all_games_stats.append([player, player_stats.wins, player_stats.losses, player_stats.win_percentage,
                                      player_stats.avg_score, player_stats.total_differential,
                                      player_stats.avg_win_differential, player_stats.high_score,
                                      player_stats.lowest_score, player_stats.total_ots])

        df2 = pd.DataFrame(all_games_stats, columns=['Player', 'Ws', 'Ls', 'Win %', 'AVG',
                                                   'Differential', 'AVG Win Differential', 'High Score',
                                                   'Low Score', 'OTs'])
        df2.to_csv('../produced_docs/Player Stats ' + self.season_name + '.csv')