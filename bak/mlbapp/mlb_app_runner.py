import time

""" OLED SETUP """
from . import esp32cam_oled as myoled

try:
    
    time.sleep(1)
      
    def fill_show():
        myoled.oled.fill(0)
        myoled.oled.show()

    """ NETWORK SETUP """
    from . import network_setup
    time.sleep(2)

    """ NTP SETUP """
    from . import ntp_setup
    from .ntp_setup import now_date
    time.sleep(2)

    """ MLB SETUP """
    from . import my_mlb_api

    """ Your Team's id """
    tm_id = 111
    start = 0
    delta = 14


    def get_score():
            
            """ Team Ids """
            home_id = games[0]["home_id"]
            away_id = games[0]["away_id"]
                    
            import ujson
            with open("/mlbapp/team_ids.py") as f:
                all_teams = f.read()
            all_team_ids = ujson.loads(all_teams)
            team1 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == home_id][0]).upper()
            team2 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == away_id][0]).upper()
            
            """ Score """
            team1_score = games[0]["home_score"]
            team2_score = games[0]["away_score"]

            """ Results """
            if team1_score > team2_score:
                team1_res = "W"
                team2_res = "L"
            else:
                team1_res = "L"
                team2_res = "W"
            """ Where """
            team1w = 'Home'
            team2w = 'Away'

            """ Statuses
                "Scheduled"
                "Pre-Game"
                "Warmup"
                "Final"
                "Game Over"
            """

            """ Status Check """
            game_status = games[0]["status"]
            if game_status == "In Progress":
                
                in_sta = games[0]["inning_state"][:3]
                inn_cur = games[0]["current_inning"]
                fill_show()
                myoled.oled.text(f"{mt}-{dy}-{short_yr}",  0, start + (0 * delta))
                myoled.oled.text(f"{hr}:{mn}"       , 72, start + (0 * delta))
                myoled.oled.text(f"{team1}: {team1_score} ({team1w})", 0, start + (1 * delta) + 2)
                myoled.oled.text(f"{team2}: {team2_score} ({team2w})", 0, start + (2 * delta)    )
                myoled.oled.text(f"Inn: {in_sta} of {inn_cur}", 0, start + (3 * delta))
                myoled.oled.text(f"Stat: {game_status}", 0, start + (4 * delta))
                myoled.oled.show()
                return 120 # check back every 120 seconds during game
            
            else:
                
                fill_show()
                myoled.oled.text(f"{mt}-{dy}-{short_yr}",  0, start + (0 * delta))
                myoled.oled.text(f"{team1}: {team1_score} ({team1w}) ", 0, start + (1 * delta) + 2)
                myoled.oled.text(f"{team2}: {team2_score} ({team2w}) ", 0, start + (2 * delta)    )
                myoled.oled.text(f"Stat: {game_status}", 0, start + (4 * delta))
                myoled.oled.show()
                return 60*30 # check back 30 min  from now

    def no_gm():
        print(f"No Game today!")
        yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
        myoled.oled.text(f"{mt}-{dy}-{short_yr}", 0, start + (0 * delta))
        myoled.oled.text(f"No Game Today!", 0, start + (1 * delta) + 2)
        myoled.oled.show()

    while True:
        
        yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
        short_yr = f"{int( str(yr)[2:]):02d}"
        
        #gm_dt = f"{mt}/{dy}/{yr}"
        gm_dt=now_date
        games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=tm_id)
        if not games:
            no_gm()
            time.sleep(60 * 240)  # check back 4 hours from now
        else:
            what_sleep=get_score()
            print(f"Sleeping {what_sleep} seconds")
            time.sleep(what_sleep)

except Exception as e:
    print(str(e))
    myoled.oled.text(str(e), 0, 0 )
    myoled.oled.show()