"""MLB API service for BB-ESP32-KIOSK."""

import urequests
import ujson
from ..models.game import GameState
from ..config.constants import MLB_API_BASE_URL, HTTP_HEADERS

class MLBApiService:
    """Service for interacting with the MLB API."""

    def __init__(self, team_id):
        """Initialize the service with a team ID."""
        self.team_id = team_id

    def get_game_data(self, game_id):
        """Get current game state from MLB API."""
        url = (f"{MLB_API_BASE_URL}/api/v1.1/game/{game_id}/feed/live?"
               "fields=gamePk,liveData,plays,currentPlay,result,description,"
               "awayScore,homeScore,about,matchup,count,inning,halfInning")

        response = urequests.get(url, headers=HTTP_HEADERS)
        data = ujson.loads(response.text)

        current_play = data['liveData']['plays']['currentPlay']
        game_status = data['gameData']['status']['detailedState']

        # Handle review/challenge states
        if 'hallenge' in game_status:
            game_status = 'Manager Challenge'
        elif 'eview' in game_status:
            game_status = 'Umpire Review'

        # Get runner information
        runners = current_play['matchup']
        bases = {
            '1st': runners.get('postOnFirst', {}).get('fullName'),
            '2nd': runners.get('postOnSecond', {}).get('fullName'),
            '3rd': runners.get('postOnThird', {}).get('fullName')
        }

        game_state = GameState(
            home_score=current_play['result']['homeScore'],
            away_score=current_play['result']['awayScore'],
            inning=current_play['about']['inning'],
            half_inning=current_play['about']['halfInning'],
            outs=current_play['count']['outs'],
            balls=current_play['count']['balls'],
            strikes=current_play['count']['strikes'],
            bases=bases,
            status=game_status
        )
        game_state.current_play = current_play['result'].get('description', '')
        return game_state

    def get_schedule(self, date):
        """Get team's schedule for a specific date."""
        params = {
            'teamId': self.team_id,
            'startDate': date,
            'endDate': date,
            'sportId': '1',
            'hydrate': 'decisions,linescore'
        }

        # Convert params to query string
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        url = f"{MLB_API_BASE_URL}/api/v1/schedule?{query}"

        response = urequests.get(url, headers=HTTP_HEADERS)
        data = ujson.loads(response.text)

        return data.get('dates', [{}])[0].get('games', [])
