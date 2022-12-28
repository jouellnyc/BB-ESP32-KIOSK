#!/usr/bin/env python

BASE_URL = "https://statsapi.mlb.com/api/"

ENDPOINTS = {
    "game": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/live",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1.1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "hydrate", "fields"],
        "required_params": [[]],
    },
    "game_timestamps": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/live/timestamps",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1.1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [],
        "required_params": [[]],
    },
    "game_boxscore": {
        "url": BASE_URL + "{ver}/game/{gamePk}/boxscore",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_content": {
        "url": BASE_URL + "{ver}/game/{gamePk}/content",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["highlightLimit"],
        "required_params": [[]],
    },
    "schedule": {
        "url": BASE_URL + "{ver}/schedule",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "scheduleType",
            "eventTypes",
            "hydrate",
            "teamId",
            "leagueId",
            "sportId",
            "gamePk",
            "gamePks",
            "venueIds",
            "gameTypes",
            "date",
            "startDate",
            "endDate",
            "opponentId",
            "fields",
        ],
        "required_params": [["sportId"], ["gamePk"], ["gamePks"]],
    },
    "schedule_tied": {
        "url": BASE_URL + "{ver}/schedule/games/tied",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["gameTypes", "season", "hydrate", "fields"],
        "required_params": [["season"]],
    },
}