import sys
import time

""" OLED SETUP """
from .esp32cam_oled import oled  as myoled
start=0
delta=13

""" MLB SETUP """
from . import my_mlb_api
from .ntp_setup import utc_to_local

""" This is the only thing you need to lookup """
""" see team_ids.py for your teams id         """
team_id = 111


def fill_show():
    myoled.fill(0)
    myoled.show()
    
def get_x_p(pname):
    fn,ln = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

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
            
        """ Records """
        home_rec = games[0]['home_rec']
        away_rec = games[0]['away_rec']
        
        """ Statuses
            "In Progress"
            "Umpire Review"?
            "Scheduled"
            "Pre-Game"
            "Warmup"
            "Final"
            "Game Over"
        """

        """ Status Check """
        game_status = games[0]["status"]
        print(games[0])
        if game_status == "In Progress" or "eview" in game_status:
            
            in_sta = games[0]["inning_state"][:3]
            inn_cur = games[0]["current_inning"]
            fill_show()
            myoled.text(f"{mt}-{dy}-{short_yr}",              0, start + (0 * delta))
            myoled.text(f"{hr}:{mn}"           ,             72, start + (0 * delta))
            myoled.text(f"{team1}: {team1_score} ({team1w})", 0, start + (1 * delta) + 2)
            myoled.text(f"{team2}: {team2_score} ({team2w})", 0, start + (2 * delta))
            myoled.text(f"Inn: {in_sta} of {inn_cur}",        0, start + (3 * delta))
            myoled.text(f"Stat: {game_status}",               0, start + (4 * delta))
            myoled.show()
            return 60 * 2 # check back every 2 minutes
        
        elif game_status == "Game Over" or game_status == "Final":
            
            lp = get_x_p(games[0]['losing_pitcher'])
            wp = get_x_p(games[0]['winning_pitcher'])
            fill_show()
            myoled.text(f"{mt}-{dy}-{short_yr} {game_status}", 0, start + (0 * delta))
            myoled.text(f"{team1}:{team1_score} H {home_rec}", 0, start + (1 * delta) + 4)
            myoled.text(f"{team2}:{team2_score} A {away_rec}", 0, start + (2 * delta))
            myoled.text(f"wp: {wp}",                           0, start + (3 * delta))
            myoled.text(f"lp: {lp}",                           0, start + (4 * delta))
            myoled.show()
            return 60 * 60 *4 # check back 4 hours from now
        
        else:
            
            fill_show()
            gm_time=games[0].get('game_datetime','NA')
            tm=utc_to_local(gm_time)
            myoled.text(f"{mt}-{dy}-{short_yr}" ,               0, start + (0 * delta))
            myoled.text(f"{hr}:{mn}"            ,              72, start + (0 * delta))
            myoled.text(f"{team1}  H {home_rec}",               0, start + (1 * delta) + 4)
            myoled.text(f"{team2}  A {away_rec}",               0, start + (2 * delta))
            myoled.text(f"{game_status} for" ,                  0, start + (3 * delta))
            myoled.text(f"{tm}"               ,                 0, start + (4 * delta))
            myoled.show()
            return 60 * 20 # check back every 20 minutes
        

def no_gm():
    print(f"No Game today!")
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    myoled.text(f"{mt}-{dy}-{short_yr}", 0, start + (0 * delta))
    myoled.text(f"No Game Today!", 0, start + (1 * delta) + 2)
    myoled.show()



while True:
   
    try:
        
        yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
        short_yr = f"{int( str(yr)[2:]):02d}"
        gm_dt = f"{mt}/{dy}/{yr}"
        
        params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
        games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
        if not games:
            no_gm()
            time.sleep(60 * 240)  # check back 4 hours from now
        else:
            what_sleep=get_score()
            print(f"Sleeping {what_sleep} seconds")
            time.sleep(what_sleep)

    except Exception as e:
        print(sys.print_exception(e))
        myoled.text(str(e), 0, 0 )
        myoled.show()
        sys.exit(1)
        
