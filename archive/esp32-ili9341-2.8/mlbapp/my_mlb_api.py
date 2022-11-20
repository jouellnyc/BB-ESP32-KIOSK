import sys
#import copy
import logging
import urequests as requests

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


def boxscore(
    gamePk,
    battingBox=True,
    battingInfo=True,
    fieldingInfo=True,
    pitchingBox=True,
    gameInfo=True,
    timecode=None,
):
    """Get a formatted boxscore for a given game."""
    boxData = boxscore_data(gamePk, timecode)

    rowLen = 79
    """rowLen is the total width of each side of the box score, excluding the " | " separator"""
    fullRowLen = rowLen * 2 + 3
    """fullRowLen is the full table width"""
    boxscore = ""
    """boxscore will hold the string to be returned"""

    if battingBox:
        # Add column headers
        awayBatters = boxData["awayBatters"]
        homeBatters = boxData["homeBatters"]

        # Make sure the home and away batter lists are the same length
        blankBatter = {
            "namefield": "",
            "ab": "",
            "r": "",
            "h": "",
            "rbi": "",
            "bb": "",
            "k": "",
            "lob": "",
            "avg": "",
            "ops": "",
        }

        while len(awayBatters) > len(homeBatters):
            homeBatters.append(blankBatter)

        while len(awayBatters) < len(homeBatters):
            awayBatters.append(blankBatter)

        # Get team totals
        awayBatters.append(boxData["awayBattingTotals"])
        homeBatters.append(boxData["homeBattingTotals"])

        # Build the batting box!
        for i in range(0, len(awayBatters)):
            if i == 0 or i == len(awayBatters) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

            boxscore += "{namefield:<40} {ab:^3} {r:^3} {h:^3} {rbi:^3} {bb:^3} {k:^3} {lob:^3} {avg:^4} {ops:^5} | ".format(
                **awayBatters[i]
            )
            boxscore += "{namefield:<40} {ab:^3} {r:^3} {h:^3} {rbi:^3} {bb:^3} {k:^3} {lob:^3} {avg:^4} {ops:^5}\n".format(
                **homeBatters[i]
            )
            if i == 0 or i == len(awayBatters) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

        # Get batting notes
        awayBattingNotes = boxData["awayBattingNotes"]
        homeBattingNotes = boxData["homeBattingNotes"]

        while len(awayBattingNotes) > len(homeBattingNotes):
            homeBattingNotes.update({len(homeBattingNotes): ""})

        while len(awayBattingNotes) < len(homeBattingNotes):
            awayBattingNotes.update({len(awayBattingNotes): ""})

        for i in range(0, len(awayBattingNotes)):
            boxscore += "{:<79} | ".format(awayBattingNotes[i])
            boxscore += "{:<79}\n".format(homeBattingNotes[i])

        boxscore += " " * rowLen + " | " + " " * rowLen + "\n"

    # Get batting and fielding info
    awayBoxInfo = {}
    homeBoxInfo = {}
    boxInfo = [awayBoxInfo, homeBoxInfo]
    sides = ["away", "home"]
    for infoType in ["BATTING", "FIELDING"]:
        if (infoType == "BATTING" and battingInfo) or (
            infoType == "FIELDING" and fieldingInfo
        ):
            for i in range(0, len(sides)):
                for z in (
                    x for x in boxData[sides[i]]["info"] if x.get("title") == infoType
                ):
                    boxInfo[i].update({len(boxInfo[i]): z["title"]})
                    for x in z["fieldList"]:
                        if len(x["label"] + ": " + x.get("value", "")) > rowLen:
                            words = iter(
                                (x["label"] + ": " + x.get("value", "")).split()
                            )
                            check = ""
                            lines = []
                            for word in words:
                                if len(check) + 1 + len(word) <= rowLen:
                                    if check == "":
                                        check = word
                                    else:
                                        check += " " + word
                                else:
                                    lines.append(check)
                                    check = "    " + word

                            if len(check):
                                lines.append(check)

                            for j in range(0, len(lines)):
                                boxInfo[i].update({len(boxInfo[i]): lines[j]})
                        else:
                            boxInfo[i].update(
                                {
                                    len(boxInfo[i]): x["label"]
                                    + ": "
                                    + x.get("value", "")
                                }
                            )

            if infoType == "BATTING":
                if len(awayBoxInfo):
                    awayBoxInfo.update({len(awayBoxInfo): " "})

                if len(homeBoxInfo):
                    homeBoxInfo.update({len(homeBoxInfo): " "})

    if len(awayBoxInfo) > 0:
        while len(awayBoxInfo) > len(homeBoxInfo):
            homeBoxInfo.update({len(homeBoxInfo): ""})

        while len(awayBoxInfo) < len(homeBoxInfo):
            awayBoxInfo.update({len(awayBoxInfo): ""})

        # Build info box
        for i in range(0, len(awayBoxInfo)):
            boxscore += ("{:<%s} | " % rowLen).format(awayBoxInfo[i])
            boxscore += ("{:<%s}\n" % rowLen).format(homeBoxInfo[i])
            if i == len(awayBoxInfo) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

    # Get pitching box
    if pitchingBox:
        awayPitchers = boxData["awayPitchers"]
        homePitchers = boxData["homePitchers"]

        # Make sure the home and away pitcher lists are the same length
        blankPitcher = {
            "namefield": "",
            "ip": "",
            "h": "",
            "r": "",
            "er": "",
            "bb": "",
            "k": "",
            "hr": "",
            "era": "",
        }

        while len(awayPitchers) > len(homePitchers):
            homePitchers.append(blankPitcher)

        while len(awayPitchers) < len(homePitchers):
            awayPitchers.append(blankPitcher)

        # Get team totals
        awayPitchers.append(boxData["awayPitchingTotals"])
        homePitchers.append(boxData["homePitchingTotals"])

        # Build the pitching box!
        for i in range(0, len(awayPitchers)):
            if i == 0 or i == len(awayPitchers) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

            boxscore += "{namefield:<43} {ip:^4} {h:^3} {r:^3} {er:^3} {bb:^3} {k:^3} {hr:^3} {era:^6} | ".format(
                **awayPitchers[i]
            )
            boxscore += "{namefield:<43} {ip:^4} {h:^3} {r:^3} {er:^3} {bb:^3} {k:^3} {hr:^3} {era:^6}\n".format(
                **homePitchers[i]
            )
            if i == 0 or i == len(awayPitchers) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

    # Get game info
    if gameInfo:
        z = boxData["gameBoxInfo"]
        gameBoxInfo = {}
        for x in z:
            if (
                len(x["label"] + (": " if x.get("value") else "") + x.get("value", ""))
                > fullRowLen
            ):
                words = iter(
                    (
                        x["label"]
                        + (": " if x.get("value") else "")
                        + x.get("value", "")
                    ).split()
                )
                check = ""
                lines = []
                for word in words:
                    if len(check) + 1 + len(word) <= fullRowLen:
                        if check == "":
                            check = word
                        else:
                            check += " " + word
                    else:
                        lines.append(check)
                        check = "    " + word

                if len(check):
                    lines.append(check)

                for i in range(0, len(lines)):
                    gameBoxInfo.update({len(gameBoxInfo): lines[i]})
            else:
                gameBoxInfo.update(
                    {
                        len(gameBoxInfo): x["label"]
                        + (": " if x.get("value") else "")
                        + x.get("value", "")
                    }
                )

        # Build the game info box
        for i in range(0, len(gameBoxInfo)):
            boxscore += ("{:<%s}" % fullRowLen + "\n").format(gameBoxInfo[i])
            if i == len(gameBoxInfo) - 1:
                boxscore += "-" * fullRowLen + "\n"

    return boxscore


def lookup_team(lookup_value, activeStatus="Y", season=2022, sportIds=1):
    """Get a info about a team or teams based on the team name, city, abbreviation, or file code."""
    params = {
        "activeStatus": activeStatus,
        "season": season,
        "sportIds": sportIds,
        "fields": "teams,id,name,teamCode,fileCode,teamName,locationName,shortName",
    }
    r = get("teams", params)

    teams = []
    for team in r["teams"]:
        for v in team.values():
            if str(lookup_value).lower() in str(v).lower():
                teams.append(team)
                break

    return teams

def boxscore_data(gamePk, timecode=None):
    """Returns a python dict containing boxscore data for a given game."""

    boxData = {}
    """boxData holds the dict to be returned"""

    params = {
        "gamePk": gamePk,
        "fields": "gameData,game,teams,teamName,shortName,teamStats,batting,atBats,runs,hits,doubles,triples,homeRuns,rbi,stolenBases,strikeOuts,baseOnBalls,leftOnBase,pitching,inningsPitched,earnedRuns,homeRuns,players,boxscoreName,liveData,boxscore,teams,players,id,fullName,allPositions,abbreviation,seasonStats,batting,avg,ops,obp,slg,era,pitchesThrown,numberOfPitches,strikes,battingOrder,info,title,fieldList,note,label,value,wins,losses,holds,blownSaves",
    }
    if timecode:
        params.update({"timecode": timecode})

    r = get("game", params)

    boxData.update({"gameId": r["gameData"]["game"]["id"]})
    boxData.update({"teamInfo": r["gameData"]["teams"]})
    boxData.update({"playerInfo": r["gameData"]["players"]})
    boxData.update({"away": r["liveData"]["boxscore"]["teams"]["away"]})
    boxData.update({"home": r["liveData"]["boxscore"]["teams"]["home"]})

    batterColumns = [
        {
            "namefield": boxData["teamInfo"]["away"]["teamName"] + " Batters",
            "ab": "AB",
            "r": "R",
            "h": "H",
            "doubles": "2B",
            "triples": "3B",
            "hr": "HR",
            "rbi": "RBI",
            "sb": "SB",
            "bb": "BB",
            "k": "K",
            "lob": "LOB",
            "avg": "AVG",
            "ops": "OPS",
            "personId": 0,
            "substitution": False,
            "note": "",
            "name": boxData["teamInfo"]["away"]["teamName"] + " Batters",
            "position": "",
            "obp": "OBP",
            "slg": "SLG",
            "battingOrder": "",
        }
    ]
    # Add away and home column headers
    sides = ["away", "home"]
    #awayBatters = copy.deepcopy(batterColumns)
    #homeBatters = copy.deepcopy(batterColumns)
    homeBatters[0]["namefield"] = boxData["teamInfo"]["home"]["teamName"] + " Batters"
    homeBatters[0]["name"] = boxData["teamInfo"]["home"]["teamName"] + " Batters"
    batters = [awayBatters, homeBatters]

    for i in range(0, len(sides)):
        side = sides[i]
        for batterId_int in [
            x
            for x in boxData[side]["batters"]
            if boxData[side]["players"].get("ID" + str(x), {}).get("battingOrder")
        ]:
            batterId = str(batterId_int)
            namefield = (
                str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[0]
                if str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[-1]
                == "0"
                else "   "
            )
            namefield += " " + boxData[side]["players"]["ID" + batterId]["stats"][
                "batting"
            ].get("note", "")
            namefield += (
                boxData["playerInfo"]["ID" + batterId]["boxscoreName"]
                + "  "
                + boxData[side]["players"]["ID" + batterId]["position"]["abbreviation"]
            )
            if not len(
                boxData[side]["players"]["ID" + batterId]
                .get("stats", {})
                .get("batting", {})
            ):
                # Protect against player with no batting data in the box score (#37)
                continue

            batter = {
                "namefield": namefield,
                "ab": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "atBats"
                    ]
                ),
                "r": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "runs"
                    ]
                ),
                "h": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "hits"
                    ]
                ),
                "doubles": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "doubles"
                    ]
                ),
                "triples": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "triples"
                    ]
                ),
                "hr": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "homeRuns"
                    ]
                ),
                "rbi": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"]["rbi"]
                ),
                "sb": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "stolenBases"
                    ]
                ),
                "bb": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "baseOnBalls"
                    ]
                ),
                "k": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "strikeOuts"
                    ]
                ),
                "lob": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "leftOnBase"
                    ]
                ),
                "avg": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "avg"
                    ]
                ),
                "ops": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "ops"
                    ]
                ),
                "personId": batterId_int,
                "battingOrder": str(
                    boxData[side]["players"]["ID" + batterId]["battingOrder"]
                ),
                "substitution": False
                if str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[-1]
                == "0"
                else True,
                "note": boxData[side]["players"]["ID" + batterId]["stats"][
                    "batting"
                ].get("note", ""),
                "name": boxData["playerInfo"]["ID" + batterId]["boxscoreName"],
                "position": boxData[side]["players"]["ID" + batterId]["position"][
                    "abbreviation"
                ],
                "obp": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "obp"
                    ]
                ),
                "slg": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "slg"
                    ]
                ),
            }
            batters[i].append(batter)

    boxData.update({"awayBatters": awayBatters})
    boxData.update({"homeBatters": homeBatters})

    # Add team totals
    sidesBattingTotals = ["awayBattingTotals", "homeBattingTotals"]
    for i in range(0, len(sides)):
        side = sides[i]
        boxData.update(
            {
                sidesBattingTotals[i]: {
                    "namefield": "Totals",
                    "ab": str(boxData[side]["teamStats"]["batting"]["atBats"]),
                    "r": str(boxData[side]["teamStats"]["batting"]["runs"]),
                    "h": str(boxData[side]["teamStats"]["batting"]["hits"]),
                    "hr": str(boxData[side]["teamStats"]["batting"]["homeRuns"]),
                    "rbi": str(boxData[side]["teamStats"]["batting"]["rbi"]),
                    "bb": str(boxData[side]["teamStats"]["batting"]["baseOnBalls"]),
                    "k": str(boxData[side]["teamStats"]["batting"]["strikeOuts"]),
                    "lob": str(boxData[side]["teamStats"]["batting"]["leftOnBase"]),
                    "avg": "",
                    "ops": "",
                    "obp": "",
                    "slg": "",
                    "name": "Totals",
                    "position": "",
                    "note": "",
                    "substitution": False,
                    "battingOrder": "",
                    "personId": 0,
                }
            }
        )

    # Get batting notes
    awayBattingNotes = {}
    homeBattingNotes = {}
    battingNotes = [awayBattingNotes, homeBattingNotes]
    for i in range(0, len(sides)):
        for n in boxData[sides[i]]["note"]:
            awayBattingNotes.update(
                {len(battingNotes[i]): n["label"] + "-" + n["value"]}
            )

    boxData.update({"awayBattingNotes": awayBattingNotes})
    boxData.update({"homeBattingNotes": homeBattingNotes})

    # Get pitching box
    # Add column headers
    pitcherColumns = [
        {
            "namefield": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
            "ip": "IP",
            "h": "H",
            "r": "R",
            "er": "ER",
            "bb": "BB",
            "k": "K",
            "hr": "HR",
            "era": "ERA",
            "p": "P",
            "s": "S",
            "name": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
            "personId": 0,
            "note": "",
        }
    ]
    #awayPitchers = copy.deepcopy(pitcherColumns)
    #homePitchers = copy.deepcopy(pitcherColumns)
    homePitchers[0]["namefield"] = boxData["teamInfo"]["home"]["teamName"] + " Pitchers"
    homePitchers[0]["name"] = boxData["teamInfo"]["away"]["teamName"] + " Pitchers"
    pitchers = [awayPitchers, homePitchers]

    for i in range(0, len(sides)):
        side = sides[i]
        for pitcherId_int in boxData[side]["pitchers"]:
            pitcherId = str(pitcherId_int)
            if not boxData[side]["players"].get("ID" + pitcherId) or not len(
                boxData[side]["players"]["ID" + pitcherId]
                .get("stats", {})
                .get("pitching", {})
            ):
                # Skip pitcher with no pitching data in the box score (#37)
                # Or skip pitcher listed under the wrong team (from comments on #37)
                continue

            namefield = boxData["playerInfo"]["ID" + pitcherId]["boxscoreName"]
            namefield += (
                "  "
                + boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                    "note", ""
                )
                if boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                    "note"
                )
                else ""
            )
            pitcher = {
                "namefield": namefield,
                "ip": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "inningsPitched"
                    ]
                ),
                "h": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "hits"
                    ]
                ),
                "r": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "runs"
                    ]
                ),
                "er": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "earnedRuns"
                    ]
                ),
                "bb": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "baseOnBalls"
                    ]
                ),
                "k": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "strikeOuts"
                    ]
                ),
                "hr": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "homeRuns"
                    ]
                ),
                "p": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                        "pitchesThrown",
                        boxData[side]["players"]["ID" + pitcherId]["stats"][
                            "pitching"
                        ].get("numberOfPitches", 0),
                    )
                ),
                "s": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "strikes"
                    ]
                ),
                "era": str(
                    boxData[side]["players"]["ID" + pitcherId]["seasonStats"][
                        "pitching"
                    ]["era"]
                ),
                "name": boxData["playerInfo"]["ID" + pitcherId]["boxscoreName"],
                "personId": pitcherId_int,
                "note": boxData[side]["players"]["ID" + pitcherId]["stats"][
                    "pitching"
                ].get("note", ""),
            }
            pitchers[i].append(pitcher)

    boxData.update({"awayPitchers": awayPitchers})
    boxData.update({"homePitchers": homePitchers})

    # Get team totals
    pitchingTotals = ["awayPitchingTotals", "homePitchingTotals"]
    for i in range(0, len(sides)):
        side = sides[i]
        boxData.update(
            {
                pitchingTotals[i]: {
                    "namefield": "Totals",
                    "ip": str(boxData[side]["teamStats"]["pitching"]["inningsPitched"]),
                    "h": str(boxData[side]["teamStats"]["pitching"]["hits"]),
                    "r": str(boxData[side]["teamStats"]["pitching"]["runs"]),
                    "er": str(boxData[side]["teamStats"]["pitching"]["earnedRuns"]),
                    "bb": str(boxData[side]["teamStats"]["pitching"]["baseOnBalls"]),
                    "k": str(boxData[side]["teamStats"]["pitching"]["strikeOuts"]),
                    "hr": str(boxData[side]["teamStats"]["pitching"]["homeRuns"]),
                    "p": "",
                    "s": "",
                    "era": "",
                    "name": "Totals",
                    "personId": 0,
                    "note": "",
                }
            }
        )

    # Get game info
    boxData.update({"gameBoxInfo": r["liveData"]["boxscore"].get("info", [])})

    return boxData

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

