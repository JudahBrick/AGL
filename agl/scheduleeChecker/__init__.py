import pandas

games_played = pandas.read_csv("games played.csv")
print(games_played.columns)
players = games_played['Player']

# players.it
num = games_played.query('Player == "Brick"')
print(num)