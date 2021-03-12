

class PlayerPreferenceStats:

    def __init__(self, name: str, preferences: [], num_of_games: [], games: []):
        self.name = name
        self.preferences = preferences
        self.num_of_games = num_of_games
        self.games = games
        self.game_to_preference_stats_map = {}


    def match_game_amounts_with_preferences(self):
        for game in self.games:
            self.game_to_preference_stats_map[game] = game



class GamePreferenceAndAmount:
    def __init__(self, game: str, preference: int, num_of_games: int):
        self.game = game
        self.preference = preference
        self.num_of_games = num_of_games
