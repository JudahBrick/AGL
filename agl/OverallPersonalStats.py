from leagueDocs.agl.Util import win_percentage


class OverallStats:

    def __init__(self, name: str, east_division: bool):
        self.name = name
        self.east_division = east_division
        self.total_wins = 0
        self.total_losses = 0
        self.division_wins = 0
        self.out_of_division_losses = 0
        self.out_of_division_wins = 0
        self.division_losses = 0
        self.home_wins = 0
        self.home_losses = 0
        self.home_win_percent = 0
        self.away_wins = 0
        self.away_losses = 0
        self.away_win_percent = 0

    def add_result(self, won: bool, home: bool, opp_in_eastern_division: bool) -> None:
        self._add_win_loss_to_total_tally(won)
        self._add_win_loss_to_home_away_tally(won, home)
        self._add_win_loss_to_division_or_out_of_tally(won, opp_in_eastern_division)
        self.count_win_percentages()

    def _add_win_loss_to_total_tally(self, won: bool):
        if won:
            self.total_wins += 1
        else:
            self.total_losses += 1

    def _add_win_loss_to_home_away_tally(self, won: bool, home: bool):
        if won and home:
            self.home_wins += 1
        elif not won and home:
            self.home_losses += 1

        elif won and not home:
            self.away_wins += 1
        elif not won and not home:
            self.away_losses += 1

    def _add_win_loss_to_division_or_out_of_tally(self, won: bool, opp_in_eastern_division: bool):
        if self.east_division == opp_in_eastern_division:
            self._add_win_loss_to_division_tally(won)
        else:
            self._add_win_loss_to_out_of_division_tally(won)

    def _add_win_loss_to_division_tally(self, won: bool):
        if won:
            self.division_wins += 1
        else:
            self.division_losses += 1

    def _add_win_loss_to_out_of_division_tally(self, won: bool):
        if won:
            self.out_of_division_wins += 1
        else:
            self.out_of_division_losses += 1

    def count_win_percentages(self) -> None:
        self.home_win_percent = win_percentage(self.away_wins, self.home_losses)
        self.away_win_percent = win_percentage(self.away_wins, self.away_losses)

    def __str__(self) -> str:
        rtn: str = self.name + " Home " + str(self.home_wins) + "-" + str(self.home_losses) \
               + " Away " + str(self.away_wins) + "-" + str(self.away_losses)
        rtn += " \n Division " + str(self.division_wins) + "-" + str(self.division_losses)
        rtn += " \n out of Division " + str(self.out_of_division_wins) + "-" + str(self.out_of_division_losses)
        return rtn

