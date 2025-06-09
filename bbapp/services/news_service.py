"""News service for BB-ESP32-KIOSK."""

from typing import List, Optional
import urequests
from ..config.constants import NEWS_URL, HTTP_HEADERS

class NewsService:
    """Service for fetching MLB news."""
    
    def __init__(self):
        """Initialize the news service."""
        self.news_url = NEWS_URL
        
    def get_latest_news(self) -> List[str]:
        """Fetch the latest MLB news."""
        pass  # To be implemented
