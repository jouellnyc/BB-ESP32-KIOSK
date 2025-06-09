"""Game state models for BB-ESP32-KIOSK."""

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class GameState:
    """Represents the current state of a baseball game."""
    home_score: int
    away_score: int
    inning: int
    half_inning: str
    outs: int
    balls: int
    strikes: int
    bases: Dict[str, Optional[str]]
    status: str  # Adding status field

    @property
    def is_final(self) -> bool:
        """Check if the game is in final state.

        Returns:
            bool: True if game status is "Game Over" or "Final", False otherwise
        """
        return self.status in ["Game Over", "Final"]

    @property
    def is_in_progress(self) -> bool:
        """Check if the game is in progress.

        Returns:
            bool: True if game is actively being played, False otherwise
        """
        return any(status in self.status for status in ["In Progress", "Review", "Challenge"])

    @property
    def is_scheduled(self) -> bool:
        """Check if the game is scheduled but not yet started.

        Returns:
            bool: True if game is scheduled but not started, False otherwise
        """
        return self.status in ["Scheduled", "Pre-Game", "Warmup"]
