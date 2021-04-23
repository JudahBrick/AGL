from typing import List, Any

import pandas as pd
import matplotlib.pyplot as plt
from leagueDocs.agl.AGL import AGL
from leagueDocs.agl.SeasonStatsPrinter import SeasonStatsPrinter
from leagueDocs.agl.analysis.ExpectedVsActualRecord import ExpectedVsActualRecord
from statistics import mean, median, mode, stdev



# the games that are legal and in the league
gameNames = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong', 'Darts',
             'Knockout', 'Pool', "Word_Hunt", "Word Bites", "Golf"]
# players in current season
# playerNames = ["Kim & Ron", "SOAs", "C & K", "NCHs", "P^5", "BFTs", "2-10ers 1CP", "PTCs"]

# current season's east players
# east = ["Kim & Ron", "SOAs", "C & K", "NCHs"]

playerNames = ["Ezra", "Moshe", "Dani", "Gavi", "Ennis", "Ilan", "Shmuli", "Hagler", "Judah",
               "Dave", "Goldstein", "Siegel", "Alyssa", "MBT", "Yitzie", "Zach", "Brick", "Elie"]
easternDivision = ["Yitzie", "Zach", "Goldstein", "Brick", "Elie", "Siegel", "Alyssa", "Dave"]
aglS6 = pd.read_csv('/Users/yehudabrick/PycharmProjects/git/leagueDocs/schedules/AGL Season 6 - Schedule.csv')  # read schedule tab into a panda dataframe
aglS6 = aglS6.drop(columns=['Games List', 'Comments', 'The Rulebook'])  # take out useless columns
aglS6 = aglS6.dropna()


# create this season's AGL POPOs
league = AGL(player_names=playerNames, games=gameNames, schedule=aglS6,
             games_per_day=14, num_of_weeks=6, east=easternDivision, season_num=6)

games_with_stats = ['Basketball', 'Cup Pong', 'Darts', 'Knockout', 'Pool', "Golf", 'Anagrams', 'Word_Hunt', 'Word Bites']

season_6_stats_printer = SeasonStatsPrinter(league=league, games_with_stats=games_with_stats,
                                            season_name='S6')
season_6_stats_printer.print()

season_6_stats_printer.write_csv_for_bar_graph()



print()
print()
print()
print("######### PRINT EVERYTHING ############")
for player in league.players:
    print()
    print()
    print(player + ":")
    print(league.players.get(player).print())
