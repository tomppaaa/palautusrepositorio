import unittest

from player import Player
from player_stats import PlayerStats


class PlayerReaderStub:
    def get_players(self):
        return [
            Player(
                {
                    "name": "Laine",
                    "nationality": "FIN",
                    "assists": 20,
                    "goals": 30,
                    "team": "CBJ",
                    "games": 70,
                    "id": 1,
                }
            ),
            Player(
                {
                    "name": "Barkov",
                    "nationality": "FIN",
                    "assists": 40,
                    "goals": 25,
                    "team": "FLA",
                    "games": 70,
                    "id": 2,
                }
            ),
            Player(
                {
                    "name": "Rantanen",
                    "nationality": "FIN",
                    "assists": 35,
                    "goals": 35,
                    "team": "COL",
                    "games": 70,
                    "id": 3,
                }
            ),
            Player(
                {
                    "name": "McDavid",
                    "nationality": "CAN",
                    "assists": 60,
                    "goals": 40,
                    "team": "EDM",
                    "games": 70,
                    "id": 4,
                }
            ),
            Player(
                {
                    "name": "Draisaitl",
                    "nationality": "DEU",
                    "assists": 50,
                    "goals": 35,
                    "team": "EDM, PIT",
                    "games": 70,
                    "id": 5,
                }
            ),
        ]


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.stats = PlayerStats(PlayerReaderStub())

    def test_top_scorers_by_nationality_are_in_descending_points_order(self):
        players = self.stats.top_scorers_by_nationality("FIN")

        self.assertEqual(
            [player.name for player in players],
            ["Rantanen", "Barkov", "Laine"],
        )

    def test_top_scorers_by_team_match_any_team_for_a_player(self):
        players = self.stats.top_scorers_by_team("PIT")

        self.assertEqual([player.name for player in players], ["Draisaitl"])

    def test_top_scorers_by_team_are_in_descending_points_order(self):
        players = self.stats.top_scorers_by_team("EDM")

        self.assertEqual(
            [player.name for player in players],
            ["McDavid", "Draisaitl"],
        )
