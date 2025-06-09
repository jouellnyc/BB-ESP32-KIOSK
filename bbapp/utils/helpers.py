"""Helper utilities for BB-ESP32-KIOSK."""

import logging
from typing import Optional

def setup_logging(debug: bool = False) -> logging.Logger:
    """Configure application logging.
    
    Args:
        debug: Whether to enable debug logging.
        
    Returns:
        Configured logger instance.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('bbkiosk')

def format_player_name(full_name: str) -> str:
    """Format a player's full name to abbreviated form.
    
    Args:
        full_name: Player's full name (e.g., "John Smith")
        
    Returns:
        Abbreviated name (e.g., "J.Smith")
    """
    fn, *ln = full_name.split(' ')
    return f"{fn[0]}.{''.join(ln)}"
