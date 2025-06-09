"""Constants used throughout the BB-ESP32-KIOSK application."""

from typing import Dict

# API Constants
MLB_API_BASE_URL = 'https://statsapi.mlb.com/api/v1.1'
OD_URL = 'https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
NEWS_URL = "https://www.mlb.com/news/"
OPENING_DAY = 'March 30'

# HTTP Headers
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
HTTP_HEADERS = {'User-Agent': USER_AGENT}

# Display Constants
ORDINALS: Dict[int, str] = {
    1: 'st', 2: 'nd', 3: 'rd', 
    4: 'th', 5: 'th', 6: 'th',
    7: 'th', 8: 'th', 9: 'th',
    10: 'th', 11: 'th', 12: 'th'
}
