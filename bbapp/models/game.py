"""Game state models for BB-ESP32-KIOSK."""

class GameState:
    """Represents the current state of a baseball game."""

    def __init__(self, home_score, away_score, inning, half_inning,
                 outs, balls, strikes, bases, status):
        """Initialize the game state."""
        self.home_score = home_score
        self.away_score = away_score
        self.inning = inning
        self.half_inning = half_inning
        self.outs = outs
        self.balls = balls
        self.strikes = strikes
        self.bases = bases
        self.status = status
        self.current_play = None  # Will be set by MLBApiService

    @property
    def is_final(self):
        """Check if the game is in final state."""
        return self.status in ["Game Over", "Final"]

    @property
    def is_in_progress(self):
        """Check if the game is in progress."""
        return any(status in self.status for status in ["In Progress", "Review", "Challenge"])

    @property
    def is_scheduled(self):
        """Check if the game is scheduled but not yet started."""
        return self.status in ["Scheduled", "Pre-Game", "Warmup"]
