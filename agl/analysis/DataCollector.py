class DataCollector:
    def __init__(self, game_list: []):
        self.map_game_name_to_list_of_scores = {}
        for game in game_list:
            self.map_game_name_to_list_of_scores[game] = []

    def add_result(self, game: str, player_score: int):
        if player_score >= 0:
            self.map_game_name_to_list_of_scores.get(game).append(player_score)

    def get_all_avgs(self):
        score_averages = {}
        for game in self.map_game_name_to_list_of_scores:
            scores = self.map_game_name_to_list_of_scores.get(game)
            score_averages[game] = average(scores)
        return score_averages

    def get_avg_for_game(self, game: str) -> int:
        return average(self.map_game_name_to_list_of_scores[game])

    def get_all_scores_for_a_game(self, game: str) -> []:
        return self.map_game_name_to_list_of_scores[game]

def average(lst):
    if len(lst) == 0:
        return -1
    return sum(lst) / len(lst)
