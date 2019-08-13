from AGL import StatsPerGame


class PlayerVsPlayerStats:

    def __init__(self, name: str, games: [], players: []):
        self.name = name
        self.vs_others = {}
        self.overall_per_player = {}
        for player in players:
            if player == name:
                continue
            self.overall_per_player[player] = StatsPerGame.StatsPerGame(player)
            for game in games:
                self.vs_others[player + "_" + game] = StatsPerGame.StatsPerGame(player + "_" + game)

    def __str__(self):
        string = ""
        for stats in self.overall_per_player:
            string += self.overall_per_player[stats].__str__() + "\n"
        for stats in self.vs_others:
            string += self.vs_others[stats].__str__() + "\n"
        return string