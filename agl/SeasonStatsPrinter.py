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
                if player_stats.wins + player_stats.losses > 0:

                    all_games_stats.append([player, player_stats.wins, player_stats.losses,
                                            round(player_stats.win_percentage, 3),
                                            round(player_stats.avg_score, 3),
                                            round(player_stats.total_differential, 3),
                                            round(player_stats.avg_win_differential, 3),
                                            round(player_stats.high_score, 3),
                                            round(player_stats.lowest_score, 3), player_stats.total_ots])

        df2 = pd.DataFrame(all_games_stats, columns=['Player', 'Ws', 'Ls', 'Win %', 'AVG',
                                                   'Differential', 'AVG Win Differential', 'High Score',
                                                   'Low Score', 'OTs'])
        df2.to_csv('/Users/yehudabrick/PycharmProjects/git/leagueDocs/produced_docs/Player Stats ' + self.season_name + '.csv')

    def write_csv_for_bar_graph(self):
        all_percentages = []
        num_of_games: int = 0;
        for player_name in self.league.players:
            player = self.league.players[player_name]
            percentage_list: [] = player.list_of_win_percentage

            # Lets find the number of game played by the players
            if len(percentage_list) > num_of_games:
                num_of_games = len(percentage_list)

            percentage_list.insert(0, player.name)
            percentage_list.insert(1, "pic")
            all_percentages.append(percentage_list)
        header: [] = []
        for i in range(num_of_games):
            header.append(i + 1)

        header.insert(0, "name")
        header.insert(0, "pic")

        df_to_csv = pd.DataFrame(all_percentages, columns=header)
        df_to_csv.to_csv('/Users/yehudabrick/PycharmProjects/git/leagueDocs/produced_docs/graphs/rank by percentage ' + self.season_name + '.csv')

