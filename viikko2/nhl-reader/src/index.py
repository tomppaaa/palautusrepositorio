from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from player_reader import PlayerReader
from player_stats import PlayerStats


SEASONS = [
    "2018-19",
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
    "2024-25",
    "2025-26",
]


def print_players(console, players, season, nationality):
    table = Table(title=f"Season {season} players from {nationality}")
    table.add_column("Player")
    table.add_column("Teams")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for player in players:
        points = player.goals + player.assists
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(points),
        )

    console.print(table)


def main():
    console = Console()
    console.print("[bold]NHL player statistics[/bold]")
    console.print("Available seasons:", ", ".join(SEASONS))
    season = Prompt.ask("Season", choices=SEASONS, default="2024-25")
    nationality = Prompt.ask(
        "Nationality (for example FIN, SWE or CAN)"
    ).upper()

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    print_players(console, players, season, nationality)


if __name__ == "__main__":
    main()
