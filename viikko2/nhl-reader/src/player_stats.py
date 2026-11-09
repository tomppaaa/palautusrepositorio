class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players = [
            player for player in self.players
            if player.nationality == nationality
        ]
        return sorted(
            players,
            key=lambda player: player.goals + player.assists,
            reverse=True,
        )

    def top_scorers_by_team(self, team):
        """Palauttaa joukkueen pelaajat pisteiden mukaan laskevassa järjestyksessä."""
        players = [
            player for player in self.players
            if team in [player_team.strip() for player_team in player.team.split(",")]
        ]
        return sorted(
            players,
            key=lambda player: player.goals + player.assists,
            reverse=True,
        )

    def top_goal_scorers(self, how_many):
        """Palauttaa how_many eniten maaleja tehnyttä pelaajaa.

        Pelaajat palautetaan maalimäärän mukaan laskevassa järjestyksessä.
        """
        return sorted(
            self.players,
            key=lambda player: player.goals,
            reverse=True,
        )[:how_many]
