"""Configuration settings for the BB-ESP32-KIOSK application."""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DisplayConfig:
    """Display-related configuration settings."""
    start: int = 5
    delta: int = 45
    debug: bool = False

@dataclass
class AppConfig:
    """Main application configuration settings."""
    force_offseason: bool = False
    test_regular_season: bool = False
    debug: bool = True
    display: DisplayConfig = DisplayConfig()
