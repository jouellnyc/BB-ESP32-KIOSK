"""Main application runner for BB-ESP32-KIOSK."""

import utime
import time
import gc
from typing import Optional, Dict

from hardware.screen_runner import display as d
from .config.constants import (
    MLB_API_BASE_URL,
    HTTP_HEADERS,
    ORDINALS,
    TEAM_COLORS
)
from .config.settings import DEBUG, FORCE_OFFSEASON, TEST_REGULAR_SEASON
from .models.game import GameState
from .display.renderer import DisplayRenderer
from .services.mlb_api import MLBApiService
from .services.news_service import NewsService
from .team_id import team_id, team_name, team_code
from .time_funcs import dy, mt, short_yr, game_day_now_nult, utc_to_local, tz_name
from .version import version

class BBKiosk:
    """Main kiosk application class."""

    def __init__(self):
        """Initialize the kiosk application."""
        self.display = DisplayRenderer(d)
        self.mlb_service = MLBApiService(team_id)
        self.news_service = NewsService()
        self.previous_play = None
        self.game_state: Optional[GameState] = None
        self._setup_team_colors()

    def _setup_team_colors(self) -> None:
        """Set up team colors for display."""
        r, g, b = TEAM_COLORS[team_code.upper()]
        self.team_color = d.color565(r, g, b)

    def check_season(self) -> None:
        """Check the current MLB season status and handle accordingly."""
        if ((int(mt) in [4, 5, 6, 7, 8, 9, 10]) or
            (int(mt) == 3 and int(dy) in [30, 31])):
            print("It's the Regular Season") if DEBUG else None
            self.run_regular_season()
        elif ((int(mt) == 2 and int(dy) in [23, 24, 25, 26, 27, 28, 29]) or
              (int(mt) == 3 and int(dy) < 30)):
            print("It's probably Spring Training") if DEBUG else None
            self.run_regular_season()
        else:
            print("Off Season") if DEBUG else None
            self.run_off_season()

    def run_regular_season(self) -> None:
        """Handle regular season game display and updates."""
        games = self.mlb_service.get_schedule(game_day_now_nult())

        if not games:
            self.show_no_game()
            return

        game_id = games[0]['game_id']
        while True:
            try:
                self.game_state = self.mlb_service.get_game_data(game_id)

                if self.game_state.is_final:
                    self.show_final_game()
                    self.show_filler_news()
                    break

                elif self.game_state.is_in_progress:
                    self.show_in_progress_game()
                    time.sleep(5)  # Check for updates every 5 seconds

                else:  # Scheduled, Pre-Game, etc.
                    self.show_scheduled_game(games[0])
                    self.show_filler_news()
                    time.sleep(60 * 5)  # Check back in 5 minutes

            except (OSError, ValueError) as e:
                print(f"Error updating game: {e}")
                self.handle_error(e)
                break

    def show_in_progress_game(self) -> None:
        """Display current game state for in-progress game."""
        if not self.game_state:
            return

        self.display.draw_game_state(
            self.game_state,
            {"home": self.team_color, "away": self.team_color}
        )

        # Show current play if it changed
        current_play = self.game_state.current_play
        if current_play != self.previous_play:
            self.display.clear_story_area()
            self.display.draw_text(
                5, self.display.start,
                current_play,
                self.display.date_font,
                self.display.white,
                self.display.drk_grn
            )
            self.previous_play = current_play

    def show_final_game(self) -> None:
        """Display final game results."""
        if not self.game_state:
            return

        self.display.draw_game_state(
            self.game_state,
            {"home": self.team_color, "away": self.team_color}
        )

    def show_scheduled_game(self, game_data: Dict) -> None:
        """Display scheduled game information."""
        game_time = utc_to_local(game_data.get('game_datetime', 'NA'))

        self.display.clear_screen()
        self.display.draw_text(
            5, self.display.start,
            f"Scheduled {mt}-{dy}-{short_yr}",
            self.display.date_font,
            self.display.white,
            self.display.drk_grn
        )
        self.display.draw_text(
            5, self.display.start + 70,
            f"Game at {game_time} {tz_name}",
            self.display.sm_font,
            self.display.white,
            self.display.drk_grn
        )

    def show_no_game(self) -> None:
        """Display no game scheduled message."""
        self.display.clear_screen()
        self.display.draw_text(
            5, 5,
            f"No {team_name} Game Today!",
            self.display.score_font,
            self.display.white,
            self.team_color
        )
        time.sleep(7)
        self.show_filler_news()

    def run_off_season(self) -> None:
        """Handle off-season display."""
        self.display.clear_screen()
        self.display.draw_text(
            5, self.display.start,
            "Off Season",
            self.display.score_font,
            self.display.white,
            self.team_color
        )
        time.sleep(30)
        self.show_filler_news()

    def show_filler_news(self) -> None:
        """Show news stories during downtime."""
        try:
            stories = self.news_service.get_latest_news()
            for story in stories:
                formatted_story = self.news_service.format_story(story)
                self.display.clear_story_area()
                self.display.draw_text(
                    5, self.display.start,
                    formatted_story,
                    self.display.date_font,
                    self.display.white,
                    self.display.drk_grn
                )
                time.sleep(7)
        except Exception as e:
            print(f"Error showing news: {e}")

    def handle_error(self, error: Exception) -> None:
        """Handle various error conditions."""
        if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(error):
            # Known ESP32 SSL issue - requires reboot
            import machine
            machine.reset()
        elif 'BadStatusLine' in str(error):
            self.display.clear_screen()
            self.display.draw_text(
                5, 80,
                "HTTP error - retrying...",
                self.display.date_font,
                self.display.white,
                self.display.drk_grn
            )
            time.sleep(60)
        else:
            print(f"Unhandled error: {error}")

    def run(self) -> None:
        """Main application loop."""
        print(f"==== Version: {version}")

        while True:
            try:
                if FORCE_OFFSEASON:
                    self.run_off_season()
                elif TEST_REGULAR_SEASON:
                    self.test_regular_season()
                else:
                    self.check_season()

                gc.collect()  # Memory management

            except Exception as e:
                self.handle_error(e)
                continue

def main():
    """Application entry point."""
    kiosk = BBKiosk()
    kiosk.run()

if __name__ == "__main__":
    main()
