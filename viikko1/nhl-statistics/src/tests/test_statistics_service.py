import unittest

from player import Player
from statistics_service import SortBy, StatisticsService


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri", "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89),
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_player_by_name(self):
        player = self.stats.search("Kurri")

        self.assertEqual(player.name, "Kurri")

    def test_search_returns_none_when_player_is_not_found(self):
        self.assertIsNone(self.stats.search("Ovechkin"))

    def test_team_returns_players_from_requested_team(self):
        players = self.stats.team("EDM")

        self.assertEqual(
            [player.name for player in players],
            ["Semenko", "Kurri", "Gretzky"],
        )

    def test_team_returns_empty_list_when_team_is_not_found(self):
        self.assertEqual(self.stats.team("NYR"), [])

    def test_top_returns_players_in_points_order(self):
        players = self.stats.top(2)

        self.assertEqual(
            [player.name for player in players],
            ["Gretzky", "Lemieux", "Yzerman"],
        )

    def test_top_returns_players_in_goals_order(self):
        players = self.stats.top(2, SortBy.GOALS)

        self.assertEqual(
            [player.name for player in players],
            ["Lemieux", "Yzerman", "Kurri"],
        )

    def test_top_returns_players_in_assists_order(self):
        players = self.stats.top(2, SortBy.ASSISTS)

        self.assertEqual(
            [player.name for player in players],
            ["Gretzky", "Yzerman", "Lemieux"],
        )
