def clean_score(score: str):
    score = score.lower()
    score = score.replace(',', '')
    return score


def is_game_scored(score: str):
    if score.__contains__('not scored') or score.__contains__('n/a') or score.__len__() == 0:
        return False

class StatsPerGame:
    first_to_win_games = ['Cup Pong', 'Darts', 'Pool']
    scored_games = ['Anagrams', "Word_Hunt", 'Word Bites', 'Archery', 'Knockout', "Shuffleboard"]

    def __init__(self, game: str, playerNames=[]):
        self.playerNames = playerNames
        self.game = game
        self.wins = 0
        self.losses = 0
        self.win_percentage = 0

        #  should be int max / min
        self.high_score = -1111111
        self.lowest_score = 11111111

        self.avg_score = 0
        self.avg_win_score = 0
        self.avg_win_differential = 0

        self.total_differential = 0
        self.total_win_differential = 0
        # todo total loss diffrential
        self.total_score_tally = 0
        self.total_loss_score = 0
        self.total_wins_score = 0
        self.total_ots = 0
        self.eight_ball_tap_ins = 0
        self.games_played = []

    def add_result(self, won: bool, score: str) -> None:
        score = clean_score(score)
        self.add_win_or_loss_tally(won)
        if is_game_scored(score) is False:
            return
        self.add_num_of_ots(score)



        if self.game == 'Basketball' or self.game == 'Shuffleboard' or self.game == 'Golf':
            self.parse_basketball_shuffelboard_or_golf(score, won)
        elif self.game == 'Pool':
            self.parse_pool(score, won)
        elif self.game == 'Anagrams' or self.game == 'Word_Hunt' or self.game == 'Word Bites':
            self.parse_word_games(score, won)
        elif self.game == 'Knockout':
            self.parse_knockout(score, won)
        elif self.first_to_win_games.__contains__(self.game):
            self.parse_first_to_win_games(score=score, won=won)
        self.calculate_avgs()

    def add_win_or_loss_tally(self, won: bool) -> None:
        if won:
            self.wins += 1
        else:
            self.losses += 1

    def is_game_scored(score: str):
        if score.__contains__('not scored') or score.__contains__('n/a') or score.__len__() == 0:
            return False

    def add_num_of_ots(self, score: str) -> None:
        if (self.game == 'Anagrams'
                or self.game == 'Word_Hunt'
                or self.game == 'Word Bites'
                or self.game == 'Knockout'):
            self.add_num_of_ots_for_scored_best_of_3_games(score)
        elif self.game == 'Basketball' or self.game == 'Shuffleboard' or self.game == 'Golf':
            self.add_num_of_ots_for_scored_single_games(score)
        else:
            self.add_num_of_ots_to_first_to_win_games(score)

    def add_num_of_ots_for_scored_best_of_3_games(self, score: str) -> None:
        games = score.split(":")
        num_of_games = games.__len__()
        if num_of_games > 3:
            self.total_ots += (num_of_games - 3)

    def add_num_of_ots_for_scored_single_games(self, score: str) -> None:
        games = score.split(":")
        num_of_games = games.__len__()
        if num_of_games > 1:
            self.total_ots += (num_of_games - 1)

    def add_num_of_ots_to_first_to_win_games(self, score: str) -> None:
        ot_arr = score.split("ot")
        num_of_games = ot_arr.__len__()

        # if there was OT
        if num_of_games > 1:
            num_of_ots = float(ot_arr[0])
            self.total_ots += num_of_ots

    def parse_scored_game(self, score: str, won: bool):
        games = score.split(":")
        num_of_games = games.__len__()


    # score is the string value from the "score" column in the schedule tab on the doc

    def parse_basketball_shuffelboard_or_golf(self, score: str, won: bool) -> None:
        # if a game went into OT then multiple games would appear separated by a ":"
        games = score.split(":")

        # set variables for checking later
        num_of_games = games.__len__()
        total_score = 0
        total_opponent_score = 0

        # if number of games is greater than 1 that means we had OT
        # todo suffleboard is best 2/3 so this OT count is false
        if num_of_games > 1:
            self.total_ots += (num_of_games - 1)

        for game in games:
            myscore = 0
            other_score = 0
            individual_score = game.split("-")
            # if a player won then their score is on the left
            if won:
                myscore = int(individual_score[0])
                other_score = int(individual_score[1])
                self.total_wins_score += myscore
                self.total_win_differential += myscore - other_score
            # if a player lost then their score is on the right
            else:
                myscore = int(individual_score[1])
                other_score = int(individual_score[0])
                self.total_loss_score += myscore

            # new high score/ low score
            self.check_for_new_high_or_low_score(myscore)

            self.total_score_tally += myscore
            self.total_differential += myscore - other_score
            # this for our data collection
            # we are trying to collect general scores of eac game so we can see what an avg
            # league score is in each game
            from leagueDocs.agl import AGL
            AGL.data_collector.add_result(self.game, myscore)

    # score is the string value from the "score" column in the schedule tab on the doc
    def parse_knockout(self, score: str, won: bool) -> None:
        # if a game went into OT then multiple games would appear separated by a ":"
        games = score.split(":")

        # set variables for checking later
        num_of_games = games.__len__()
        total_score = 0

        for game in games:
            myscore = 0
            other_score = 0
            individual_score = game.split("-")
            # if a player won then their score is on the left (index 0)
            if won:
                myscore = int(individual_score[0])
                other_score = int(individual_score[1])
                if myscore == 0:
                    myscore = myscore - other_score
                total_score += myscore
                # total_opponent_score += total_opponent_score
                # self.total_wins_score += myscore
                # self.total_win_differential += myscore - other_score
            # if a player lost then their score is on the right (index 1)
            else:
                myscore = int(individual_score[1])
                other_score = int(individual_score[0])
                if myscore == 0:
                    myscore = myscore - other_score
                total_score += myscore
                # total_opponent_score += total_opponent_score
                # self.total_loss_score += myscore

            # self.total_score_tally += myscore
            # self.total_differential += myscore - other_score

        # new high score/ low score
        self.check_for_new_high_or_low_score(total_score)

        if won:
            self.total_wins_score += total_score
        else:
            self.total_loss_score += total_score

        self.total_score_tally += total_score
        self.total_differential += total_score

        # this for our data collection
        # we are trying to collect general scores of eac game so we can see what an avg
        # league score is in each game
        from leagueDocs.agl import AGL
        AGL.data_collector.add_result(self.game, total_score)

    def parse_first_to_win_games(self, score: str, won: bool) -> None:
        ot_arr = score.split("ot")
        num_of_games = ot_arr.__len__()

        # if there was OT
        if num_of_games > 1:
            winner_score = float(ot_arr[1])

            num_of_ots = float(ot_arr[0])
            self.total_ots += num_of_ots
        else:
            winner_score = float(ot_arr[0])

        if won:
            self.total_wins_score += winner_score
            self.total_win_differential += winner_score
            self.total_differential += winner_score
            if winner_score > self.high_score:
                self.high_score = winner_score
            if winner_score < self.lowest_score:
                self.lowest_score = winner_score
        else:
            winner_score = 0 - winner_score
            self.total_differential += winner_score
            self.total_loss_score += winner_score
            if winner_score < self.lowest_score:
                self.lowest_score = winner_score
            if winner_score > self.high_score:
                self.high_score = winner_score

        self.total_score_tally += winner_score
        # python doesn't allow circular dependencies,
        # but if I do the import here instead of on top it works
        from leagueDocs.agl import AGL
        AGL.data_collector.add_result(self.game, winner_score)

    def parse_pool(self, score: str, won: bool) -> None:
        if score.__contains__('8-ball'):
            # print(score)
            ball_tap_in = score.split(':')
            # print(ball_tap_in[1])
            new_score = ball_tap_in[1]
            # this is a hack in order to compensate for the season 2 scoring of 8-ball tap ins
            # with this new score it assumes that winner was on the 8-bal when the loser tapped it in
            # the current (season 3 rule) would have the amount both players had
            if not new_score.__contains__('-'):
                new_score += '-0'
            self.parse_basketball_shuffelboard_or_golf(score=new_score, won=won)
        else:
            self.parse_first_to_win_games(score=score, won=won)

    def parse_word_games(self, score: str, won: bool) -> None:
        games = score.split(":")
        for game in games:
            individual_score = game.split("-")
            winning_score = int(individual_score[0])
            losing_score = int(individual_score[1])
            game_score = (winning_score - losing_score) / winning_score
            return self.parse_first_to_win_games(str(game_score), won)

    def check_for_new_high_or_low_score(self, score: int):
        if score > self.high_score:
            self.high_score = score
        if score < self.lowest_score:
            self.lowest_score = score

    def calculate_avgs(self):
        total_games = self.wins + self.losses + self.total_ots
        if total_games > 0:
            self.win_percentage = self.calculate_win_percentage(self.wins, self.losses)
            self.avg_score = self.total_score_tally / total_games

        if self.wins > 0:
            self.avg_win_score = self.total_wins_score / self.wins
            self.avg_win_differential = self.total_win_differential / self.wins

    def calculate_win_percentage(self, wins: int, losses: int) -> float:
        if wins == losses and losses == 0:
            return 0
        elif losses == 0 and wins != 0:
            return float(100)
        else:
            return round((wins / (wins + losses)) * 100, 1)

    def get_win_loss_string(self) -> str:
        return str(self.wins) + "-" + str(self.losses)

    def __str__(self) -> str:
        self.calculate_avgs()
        if self.playerNames.__contains__(self.game):
            string = self.game + ": "
            for played in self.games_played:
                string += played
                string += ", "
            return string
        return self.game + " " + str(self.wins) + ":" + str(self.losses) \
               + "   " + str(self.win_percentage) + "%" + " avg score: " + str(self.avg_score) + \
               "  diffrential score: " + str(self.total_differential) + "  avg win diffrential score: " + \
               str(self.avg_win_differential) + "  OTs: " + str(self.total_ots)
#          + " " + str(self._wins/self._losses) + "%"
