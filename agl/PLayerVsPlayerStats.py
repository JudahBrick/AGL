from leagueDocs.agl import StatsPerGame


class PlayerVsPlayerStats:

    def __init__(self, name: str, games: [], players: []):
        self.name = name
        self.vs_others = {}
        self.overall_per_player = {}

        for player in players:
            if player == name:
                continue
            self.overall_per_player[player] = StatsPerGame.StatsPerGame(player)

    def add_result(self, opponent: str, game: str, won: bool, score: str) -> None:
        search = opponent + "_" + game
        rtn = self.vs_others.get(search)
        if rtn is None:
            self.vs_others[search] = StatsPerGame.StatsPerGame(search)

        self.vs_others.get(opponent + "_" + game).add_result(won, score=score)
        str = game + " "
        if won:
            str += " won "
        else:
            str += " loss "
        str += score
        # todo Put this back in and refactor this class,
        #  took this out because it was throwing errors for the regular game stats class
        # self.overall_per_player.get(opponent).add_result(won, score=str)

    def __str__(self):
        string = ""
        for stats in self.overall_per_player:
            string += self.overall_per_player[stats].__str__() + "\n"
        for stats in self.vs_others:
            string += self.vs_others[stats].__str__() + "\n"
        return string
