"""Display rendering functionality for BB-ESP32-KIOSK."""

from typing import Optional, Dict, Any
from hardware.screen_runner import display as d
from ..models.game import GameState

class DisplayRenderer:
    """Handles all display rendering operations."""
    
    def __init__(self, display_driver: Any):
        """Initialize the renderer with a display driver."""
        self.display = display_driver
        
    def clear_screen(self) -> None:
        """Clear the entire screen."""
        self.display.clear_fill()
        
    def draw_game_state(self, state: GameState) -> None:
        """Draw the current game state on the display."""
        pass  # To be implemented
