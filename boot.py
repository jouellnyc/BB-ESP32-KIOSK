""" NETWORK SETUP """
import network_setup
import time

time.sleep(5)

""" OLED SETUP """
import myoled
time.sleep(1)


""" NTP SETUP  
# This is hard to debug if in a separate module
# And semi impossible to keep at UTC
# the esp32 cam always reverts back
# also difficult to convert UTC to localtime
# which MLB uses for gametime .. no we don't use it
# for 'now'

import ntptime
import time


try:
    ntptime.host1 = "server 3.north-america.pool.ntp.org"
    ntptime.settime()
except Exception as e:
    ntptime.host1 = "server 1.north-america.pool.ntp.org"
    ntptime.settime()
else:
    print("Local time before synchronization：%s" % str(time.localtime()))
    print("Local time after synchronization：%s" % str(time.localtime()))
time.sleep(2)
"""

""" MLB SETUP """
import time
import utime
import my_mlb_api

""" Your Team's id """
tm_id = 111
start = 0
delta = 14

def fill_show():
    myoled.oled.fill(0)
    myoled.oled.show()

def get_score():
        
        """ Team Ids """
        home_id = games[0]["home_id"]
        away_id = games[0]["away_id"]
                
        import ujson
        with open("team_ids.py") as f:
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
        team1w = 'H'
        team2w = 'A'

        """ Statuses
            "Scheduled"
            "Pre-Game"
            "Warmup"
            "Final"
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
            return 60 
        
        else:
            
            fill_show()
            myoled.oled.text(f"{mt}-{dy}-{short_yr}",  0, start + (0 * delta))
            myoled.oled.text(f"{team1}: {team1_score} ({team1_res}) ({team1w}) ", 0, start + (1 * delta) + 2)
            myoled.oled.text(f"{team2}: {team2_score} ({team2_res}) ({team2w}) ", 0, start + (2 * delta)    )
            myoled.oled.text(f"Stat: {game_status}", 0, start + (4 * delta))
            myoled.oled.show()
            return 60*30

def no_gm():
    print(f"No Game today! - {slp}")
    yr, mt, dy, hr, mn, s1, s2, s3 = utime.localtime()
    myoled.oled.text(f"{mt}-{dy}-{short_yr}", 0, start + (0 * delta))
    myoled.oled.text(f"No Game Today!", 0, start + (1 * delta) + 2)
    myoled.oled.show()

while True:
    
    yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in utime.localtime() ]
    short_yr = f"{int( str(yr)[2:]):02d}"
    
    gm_dt = f"{mt}/{dy}/{yr}"
    games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=tm_id)
    if not games:
        no_gm()
        time.sleep(60 * 240)  # check back 4 hours from now
    else:
        what_sleep=get_score()
        print(f"Sleeping {what_sleep} seconds")
        time.sleep(what_sleep)        
