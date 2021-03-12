import pandas

games_played = pandas.read_csv("games played.csv")
print(games_played.columns)
players = games_played['player']

# players.it