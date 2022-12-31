"""
Credit: https://github.com/toddrob99/MLB-StatsAPI
"""

import sys
###JJO import copy
import logging
###JJO import urequests as requests
import mrequests as requests

from . import endpoints

BASE_URL = endpoints.BASE_URL
"""Base MLB Stats API URL"""
ENDPOINTS = endpoints.ENDPOINTS
"""MLB Stats API endpoint configuration"""

logger = logging.getLogger("statsapi")


def schedule(
    date=None,
    start_date=None,
    end_date=None,
    team="",
    opponent="",
    sportId=1,
    game_id=None,
    params=None
):
    """Get list of games for a given date/range and/or team/opponent."""
    if end_date and not start_date:
        date = end_date
        end_date = Nonef

    if start_date and not end_date:
        date = start_date
        start_date = None

    #params = {}
    """
    if date:
        params.update({"date": date})
    elif start_date and end_date:
        params.update({"startDate": start_date, "endDate": end_date})

    if team != "":
        params.update({"teamId": str(team)})

    if opponent != "":
        params.update({"opponentId": str(opponent)})

    if game_id:
        params.update({"gamePks": game_id})

    params.update(
        {
            "sportId": str(sportId),
            "hydrate": "decisions,probablePitcher(note),linescore",
        }
    )
    """

    r = get("schedule", params)

    games = []
    if r.get("totalItems") == 0:
        return games  # TODO: ValueError('No games to parse from schedule object.') instead?
    else:
        for date in r.get("dates"):
            for game in date.get("games"):
                game_info = {
                    "game_id": game["gamePk"],
                    "game_datetime": game["gameDate"],
                    "game_date": date["date"],
                    "game_type": game["gameType"],
                    "status": game["status"]["detailedState"],
                    "away_name": game["teams"]["away"]["team"]["name"],
                    "home_name": game["teams"]["home"]["team"]["name"],
                    "away_id": game["teams"]["away"]["team"]["id"],
                    "home_id": game["teams"]["home"]["team"]["id"],
                    "doubleheader": game["doubleHeader"],
                    "game_num": game["gameNumber"],
                    "home_probable_pitcher": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "away_probable_pitcher": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "home_pitcher_note": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_pitcher_note": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_score": game["teams"]["away"].get("score", "0"),
                    "home_score": game["teams"]["home"].get("score", "0"),
                    "current_inning": game.get("linescore", {}).get( "currentInning", ""),
                    "inning_state": game.get("linescore", {}).get("inningState", ""),
                    "venue_id"    : game.get("venue", {}).get("id"),
                    "venue_name"  : game.get("venue", {}).get("name"),
                    "home_rec"    : str(game.get("teams", {}).get('home',{}).get('leagueRecord','').get('wins',''))  + 
                    "-" + str(game.get("teams", {}).get('home',{}).get('leagueRecord','').get('losses','')),
                    "away_rec"    : str(game.get("teams", {}).get('away',{}).get('leagueRecord','').get('wins',''))  + 
                    "-" + str(game.get("teams", {}).get('away',{}).get('leagueRecord','').get('losses','')),
                    "home_id"     : game.get("teams", {}).get('home',{}).get('team','').get('id',''),
                    "away_id"     : game.get("teams", {}).get('away',{}).get('team','').get('id',''),
                }

                if game_info["status"] in ["Final", "Game Over"]:
                    if game.get("isTie"):
                        game_info.update({"winning_team": "Tie", "losing_Team": "Tie"})
                    else:
                        game_info.update(
                            {
                                "winning_team": game["teams"]["away"]["team"]["name"]
                                if game["teams"]["away"].get("isWinner")
                                else game["teams"]["home"]["team"]["name"],
                                "losing_team": game["teams"]["home"]["team"]["name"]
                                if game["teams"]["away"].get("isWinner")
                                else game["teams"]["away"]["team"]["name"],
                                "winning_pitcher": game.get("decisions", {})
                                .get("winner", {})
                                .get("fullName", ""),
                                "losing_pitcher": game.get("decisions", {})
                                .get("loser", {})
                                .get("fullName", ""),
                                "save_pitcher": game.get("decisions", {})
                                .get("save", {})
                                .get("fullName"),
                            }
                        )
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"]["name"]
                        + " ("
                        + str(game["teams"]["away"]["score"])
                        + ") @ "
                        + game["teams"]["home"]["team"]["name"]
                        + " ("
                        + str(game["teams"]["home"]["score"])
                        + ") ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})
                elif game_info["status"] == "In Progress":
                    game_info.update(
                        {
                            "Balls"   : game.get("linescore",{}).get('balls',''),
                            "Strikes" : game.get("linescore",{}).get('strikes',''),
                            "Batter"  : game.get("linescore",{}).get('offense',{}).get('batter','').get('fullName',''),
                            "Outs"    : game.get("linescore",{}).get('outs',''),
                            "summary": date["date"]
                            + " - "
                            + game["teams"]["away"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["away"]["score"])
                            + ") @ "
                            + game["teams"]["home"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["home"]["score"])
                            + ") ("
                            + game["linescore"]["inningState"]
                            + " of the "
                            + game["linescore"]["currentInningOrdinal"] 
                            + ")" 
                        }
                    )
                else:
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"]["name"]
                        + " @ "
                        + game["teams"]["home"]["team"]["name"]
                        + " ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})

                games.append(game_info)

        return games


def get(endpoint, params, force=False):
    """Call MLB StatsAPI and return JSON data.

    This function is for advanced querying of the MLB StatsAPI,
    and is used by the functions in this library.
    """
    # Lookup endpoint from input parameter
    ep = ENDPOINTS.get(endpoint)
    if not ep:
        raise ValueError("Invalid endpoint (" + str(endpoint) + ").")

    url = ep["url"]
    logger.debug("URL: {}".format(url))

    path_params = {}
    query_params = {}

    # Parse parameters into path and query parameters, and discard invalid parameters
    for p, pv in params.items():
        if ep["path_params"].get(p):
            logger.debug("Found path param: {}".format(p))
            if ep["path_params"][p].get("type") == "bool":
                if str(pv).lower() == "false":
                    path_params.update({p: ep["path_params"][p].get("False", "")})
                elif str(pv).lower() == "true":
                    path_params.update({p: ep["path_params"][p].get("True", "")})
            else:
                path_params.update({p: str(pv)})
        elif p in ep["query_params"]:
            logger.debug("Found query param: {}".format(p))
            query_params.update({p: str(pv)})
        else:
            if force:
                logger.debug(
                    "Found invalid param, forcing into query parameters per force flag: {}".format(
                        p
                    )
                )
                query_params.update({p: str(pv)})
            else:
                logger.debug("Found invalid param, ignoring: {}".format(p))

    logger.debug("path_params: {}".format(path_params))
    logger.debug("query_params: {}".format(query_params))

    # Replace path parameters with their values
    for k, v in path_params.items():
        logger.debug("Replacing {%s}" % k)
        url = url.replace(
            "{" + k + "}",
            ("/" if ep["path_params"][k]["leading_slash"] else "")
            + v
            + ("/" if ep["path_params"][k]["trailing_slash"] else ""),
        )
        logger.debug("URL: {}".format(url))

    while url.find("{") != -1 and url.find("}") > url.find("{"):
        param = url[url.find("{") + 1 : url.find("}")]
        if ep.get("path_params", {}).get(param, {}).get("required"):
            if (
                ep["path_params"][param]["default"]
                and ep["path_params"][param]["default"] != ""
            ):
                logger.debug(
                    "Replacing {%s} with default: %s."
                    % (param, ep["path_params"][param]["default"])
                )
                url = url.replace(
                    "{" + param + "}", ep["path_params"][param]["default"]
                )
            else:
                if force:
                    logger.warning(
                        "Missing required path parameter {%s}, proceeding anyway per force flag..."
                        % param
                    )
                else:
                    raise ValueError("Missing required path parameter {%s}" % param)
        else:
            logger.debug("Removing optional param {%s}" % param)
            url = url.replace("{" + param + "}", "")

        logger.debug("URL: {}".format(url))
    # Add query parameters to the URL
    if len(query_params) > 0:
        for k, v in query_params.items():
            logger.debug("Adding query parameter {}={}".format(k, v))
            sep = "?" if url.find("?") == -1 else "&"
            url += sep + k + "=" + v
            logger.debug("URL: {}".format(url))

    # Make sure required parameters are present
    satisfied = False
    missing_params = []
    for x in ep.get("required_params", []):
        if len(x) == 0:
            satisfied = True
        else:
            missing_params.extend([a for a in x if a not in query_params])
            if len(missing_params) == 0:
                satisfied = True
                break

    if not satisfied and not force:
        if ep.get("note"):
            note = "\n--Endpoint note: " + ep.get("note")
        else:
            note = ""

        raise ValueError(
            "Missing required parameter(s): "
            + ", ".join(missing_params)
            + ".\n--Required parameters for the "
            + endpoint
            + " endpoint: "
            + str(ep.get("required_params", []))
            + ". \n--Note: If there are multiple sets in the required parameter list, you can choose any of the sets."
            + note
        )

    # Make the request
    r = requests.get(url)
    if r.status_code not in [200, 201]:
        r.raise_for_status()
    else:
        return r.json()

    return None


