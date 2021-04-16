from leagueDocs.agl import StatsPerGame
from leagueDocs.agl.GameTracker import GameTracker


class PlayerVsPlayerStats:

    def __init__(self, name: str, games: [], players: []):
        self.name = name
        self.overall_per_player = {}
        self.games_played = {}

        for player in players:
            if player == name:
                continue
            self.overall_per_player[player] = StatsPerGame.StatsPerGame(player)
            self.overall_per_player[player] = GameTracker(player)

        for game in games:
            self.games_played[game] = GameTracker(game)

    def add_result(self, opponent: str, game: str, won: bool, score: str) -> None:
        game_tracker_for_player: GameTracker = self.overall_per_player[opponent]
        game_tracker_for_player.add_result(game, won, score)

        game_tracker_for_game = self.games_played[game]
        game_tracker_for_game.add_result(game, won, score)

    def __str__(self):
        string = ""
        for player in self.overall_per_player:
            string += self.overall_per_player[player].__str__() + "\n"
        for game in self.games_played:
            string += self.games_played[game].__str__() + "\n"
        return string
