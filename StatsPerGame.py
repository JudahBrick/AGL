

class StatsPerGame:
    first_to_win_games = ['Cup Pong', 'Darts',  'Pool']
    scored_games = ['Anagrams', 'Archery', 'Knockout', "Shuffleboard", "Word_Hunt"]

    def __init__(self, game: str):
        self.game = game
        self.wins = 0
        self.losses = 0
        self.win_percentage = 0

        self.high_score = -1111111
        self.lowest_score = 11111111

        self.avg_score = 0
        self.avg_win_score = 0

        self.total_differential = 0
        self.total_score_tally = 0
        self.total_loss_score = 0
        self.total_wins_score = 0

    def add_result(self, won: bool, score: str):
        if won :
            self.wins += 1
        else:
            self.losses += 1

        if self.game == 'Basketball':
            self.parse_basketball(score, won)

    def parse_score(self, score: str, won: bool):
        if self.first_to_win_games.__contains__(self.game):
            return self.parse_first_to_win_games(score)

    def parse_first_to_win_games(self, score: str, won: bool):
        score = score.lower()
        index = score.find("ot")
        ot = False
        if index > -1:
            ot = True

    #     assuming all thats left int he string
        score.i

    def parse_scored_game(self, score: str, won: bool):
        games = score.split(":")
        num_of_games = games.__len__()

    def parse_basketball(self, score: str, won: bool):
        games = score.split(":")
        num_of_games = games.__len__()
        total_score = 0
        ot = False

        if num_of_games > 1:
            ot = True

        for game in games:
            myscore = 0
            individual_score = game.split("-")
            if won:
                myscore = int(individual_score[0])
            else:
                myscore = int(individual_score[1])
            if myscore > self.high_score:
                self.high_score = myscore
            elif myscore < self.lowest_score:
                self.lowest_score = myscore

            if won:
                self.total_wins_score += myscore
            else:
                self.total_loss_score += myscore
            total_score += myscore
            self.total_score_tally += myscore

        total_score /= num_of_games

    def calculate_avgs(self):
        total_games = self.wins + self.losses
        if total_games > 0:
            self.win_percentage = self.calculate_win_percentage(self.wins, self.losses)
            self.avg_score = self.total_score_tally / total_games

        if self.wins > 0:
            self.avg_win_score = self.total_wins_score / self.wins

    def calculate_win_percentage(self, wins: int, losses: int):
        if wins == losses and losses == 0:
            return 0
        elif losses == 0 and wins != 0:
            return float(100)
        else:
            return round((wins / (wins + losses)) * 100, 1)

    def __str__(self):
        self.calculate_avgs()
        return self.game + " " + str(self.wins) + ":" + str(self.losses) \
               + "   " + str(self.win_percentage) + "%" + " avg score: " + str(self.avg_score)
#          + " " + str(self._wins/self._losses) + "%"


