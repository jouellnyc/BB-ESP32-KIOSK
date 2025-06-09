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
    
    @property
    def is_final(self) -> bool:
        """Check if the game is in final state."""
        return False  # To be implemented
