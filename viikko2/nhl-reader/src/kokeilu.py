from player_reader import PlayerReader
from player_stats import PlayerStats


url = "https://studies.cs.helsinki.fi/nhlstats/2026-27/players"
stats = PlayerStats(PlayerReader(url))

for player in stats.top_scorers_by_team("DAL"):
    print(player)
