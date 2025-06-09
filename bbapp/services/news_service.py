"""News service for BB-ESP32-KIOSK."""

import urequests
from ..config.constants import MLB_NEWS_URL, HTTP_HEADERS

class NewsService:
    """Service for fetching MLB news."""

    def get_latest_news(self, max_stories=10):
        """Get latest MLB news stories."""
        response = urequests.get(MLB_NEWS_URL, headers=HTTP_HEADERS)

        # Parse the response and extract headlines
        stories = []
        try:
            data = response.json()
            articles = data.get('articles', [])

            for article in articles[:max_stories]:
                headline = article.get('headline', '')
                if headline:
                    stories.append(headline)

        except ValueError as e:
            print(f"Error parsing news feed: {e}")
            stories = ["Error fetching news"]

        return stories

    def format_story(self, story):
        """Format a story for display by removing unsupported characters."""
        replacements = {
            'à': 'a', 'â': 'a', 'ç': 'c', 'é': 'e', 'è': 'e',
            'ê': 'e', 'ë': 'e', 'î': 'i', 'ï': 'i', 'ô': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'À': 'A', 'Â': 'A', 'Ç': 'C', 'É': 'E', 'È': 'E',
            'Ê': 'E', 'Ë': 'E', 'Î': 'I', 'Ï': 'I', 'Ô': 'O',
            'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            '\xed': 'i', '\xe9': 'e', '\xc0': 'A',
            '\xe8': 'e', '\xec': 'i', '\xd2': 'O',
            '\xf9': 'u', '\xc9': 'E', '\xe1': 'a',
            '\xcd': 'I', '\xf3': 'o', '\xda': 'U',
            '\u2018': "'", '\u2019': "'",
            '\xa0': ' ', '\xc1': 'A', '\xf1': 'n'
        }

        for accented, non_accented in replacements.items():
            story = story.replace(accented, non_accented)

        return story
