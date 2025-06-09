"""Display rendering functionality for BB-ESP32-KIOSK."""

from typing import Optional, Dict, Any
from hardware.screen_runner import display as d
from ..models.game import GameState
from ..config.constants import ORDINALS

class DisplayRenderer:
    """Handles all display rendering operations."""

    def __init__(self, display_driver: Any):
        """Initialize the renderer with a display driver."""
        self.display = display_driver
        self.start = 5  # Starting Y position
        self.delta = 45  # Y spacing between elements

    def clear_screen(self) -> None:
        """Clear the entire screen."""
        self.display.clear_fill()

    def clear_story_area(self) -> None:
        """Clear the story display area."""
        self.display.fill_rectangle(1, 41, 318, 198, self.display.drk_grn)

    def draw_game_state(self, state: GameState, team_colors: Dict[str, int]) -> None:
        """Draw the current game state on the display.

        Args:
            state: Current game state
            team_colors: Dict mapping team codes to their display colors
        """
        self.clear_screen()

        # Draw game status and inning
        status_text = (f"{state.half_inning} {state.inning}{ORDINALS[state.inning]}"
                      if state.is_in_progress else state.status)
        self.display.draw_text(5, self.start, status_text,
                             self.display.date_font, self.display.white, self.display.drk_grn)

        # Draw scores
        self._draw_team_score("HOME", state.home_score, team_colors["home"], 1)
        self._draw_team_score("AWAY", state.away_score, team_colors["away"], 2)

        if state.is_in_progress:
            # Draw count
            self.display.draw_text(
                10, self.start + (4 * self.delta) + 5,
                f"B: {state.balls} S: {state.strikes} O: {state.outs}",
                self.display.sm_font, self.display.white, self.display.drk_grn
            )
            # Draw bases
            self._draw_bases(state.bases)

        self.display.draw_outline_box()

    def _draw_team_score(self, team: str, score: int, color: int, position: int) -> None:
        """Draw a team's score line."""
        self.display.draw_text(
            5, self.start + (position * self.delta) + 5,
            f"{team}:{score}",
            self.display.score_font, self.display.white, color
        )

    def _draw_bases(self, bases: Dict[str, Optional[str]]) -> None:
        """Draw the base diagram showing runners."""
        base_positions = {
            '1st': [4, 275, 200, 10],
            '2nd': [4, 250, 165, 10],
            '3rd': [4, 225, 200, 10]
        }

        for base, pos in base_positions.items():
            if bases.get(base):
                self._draw_filled_base(*pos)
            else:
                self._draw_empty_base(*pos)

    def _draw_filled_base(self, ax: int, bx: int, cx: int, dx: int) -> None:
        """Draw a filled base diamond."""
        self.display.fill_polygon(ax, bx, cx, dx, self.display.white, rotate=0)

    def _draw_empty_base(self, ax: int, bx: int, cx: int, dx: int) -> None:
        """Draw an empty base diamond."""
        self.display.draw_polygon(ax, bx, cx, dx, self.display.white, rotate=0)
