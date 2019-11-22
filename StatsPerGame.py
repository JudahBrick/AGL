

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
        self.avg_win_differential = 0

        self.total_differential = 0
        self.total_win_differential = 0
        self.total_score_tally = 0
        self.total_loss_score = 0
        self.total_wins_score = 0
        self.total_ots = 0
        self.eight_ball_tap_ins = 0

    def add_result(self, won: bool, score: str):
        if won :
            self.wins += 1
        else:
            self.losses += 1

        if self.game == 'Basketball' or self.game == 'Shuffleboard':
            self.parse_basketball_or_shuffelboard(score, won)
        if self.first_to_win_games.__contains__(self.game):
            self.parse_first_to_win_games(score=score, won=won)
        self.calculate_avgs()

    def parse_score(self, score: str, won: bool):
        if self.first_to_win_games.__contains__(self.game):
            return self.parse_first_to_win_games(score)

    def parse_scored_game(self, score: str, won: bool):
        games = score.split(":")
        num_of_games = games.__len__()

    def parse_basketball_or_shuffelboard(self, score: str, won: bool):
        games = score.split(":")
        num_of_games = games.__len__()
        total_score = 0
        total_opponent_score = 0
        ot = False

        if num_of_games > 1:
            ot = True

        for game in games:
            myscore = 0
            other_score = 0
            individual_score = game.split("-")
            #
            if won:
                myscore = int(individual_score[0])
                other_score = int(individual_score[1])
                self.total_wins_score += myscore
                self.total_win_differential += myscore
                self.total_win_differential -= other_score

            else:
                myscore = int(individual_score[1])
                other_score = int(individual_score[0])
                self.total_loss_score += myscore

            # new high score/ low score
            if myscore > self.high_score:
                self.high_score = myscore
            elif myscore < self.lowest_score:
                self.lowest_score = myscore

            total_score += myscore
            total_opponent_score += other_score
            self.total_score_tally += myscore
            self.total_differential += myscore
            self.total_differential -= other_score

        total_score /= num_of_games

    def parse_first_to_win_games(self, score: str, won: bool):
        # Should also write how much they usualy get on avrage.
        # meaning not just the negative of how they did but also the positive.
        score = score.lower()

        ot_arr = score.split("ot")
        num_of_games = ot_arr.__len__()

        # if there was OT
        if num_of_games > 1:
            if ot_arr[1].__contains__('8-ball'):
                ball_tap_in = ot_arr[1].split(':')
                winner_score = int(ball_tap_in[1])
                if not won:
                    self.eight_ball_tap_ins += 1
            else:
                winner_score = int(ot_arr[1])

            num_of_ots = int(ot_arr[0])
            self.total_ots += num_of_ots
        else:
            if score.__contains__('8-ball'):
                print(score)
                ball_tap_in = score.split(':')
                print(ball_tap_in[1])
                winner_score = int(ball_tap_in[1])
                if not won:
                    self.eight_ball_tap_ins += 1
            else:
                winner_score = int(ot_arr[0])

        if won:
            self.total_wins_score += winner_score
            self.total_win_differential += winner_score
            self.total_differential += winner_score
            if winner_score > self.high_score:
                self.high_score = winner_score
        else:
            winner_score = 0 - winner_score
            self.total_differential += winner_score
            self.total_loss_score += winner_score
            if winner_score < self.lowest_score:
                self.lowest_score = winner_score

        self.total_score_tally += winner_score

    def calculate_avgs(self):
        total_games = self.wins + self.losses
        if total_games > 0:
            self.win_percentage = self.calculate_win_percentage(self.wins, self.losses)
            self.avg_score = self.total_score_tally / total_games

        if self.wins > 0:
            self.avg_win_score = self.total_wins_score / self.wins
            self.avg_win_differential = self.total_win_differential / self.wins


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
               + "   " + str(self.win_percentage) + "%" + " avg score: " + str(self.avg_score) +\
               "  diffrential score: " + str(self.total_differential) + "  avg win diffrential score: " +\
               str(self.avg_win_differential) + "  OTs: " + str(self.total_ots)
#          + " " + str(self._wins/self._losses) + "%"


