#This is for a stand up case like the orange case:
#https://github.com/jouellnyc/MLB-ESP32/blob/main/images/orange.png

import sys
import time

""" OLED SETUP """
from .esp32_oled_2_8_inch import display, red, black, white, drk_grn, score_font, date_font, sm_font

""" All non caught errors are handled by main.py """  
from . team_id import team_id

start=5
delta=45

""" MLB SETUP """
from . import my_mlb_api
from .ntp_setup import utc_to_local

""" Version """
from .version import version

   
def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

def draw_outline_box():
    display.draw_vline(0, 0, 319, white)
    display.draw_vline(238, 0, 319, white)
    display.draw_hline(0, 0, 239, white)
    display.draw_hline(0,  40, 239, white)
    display.draw_hline(0, 319, 239, white)

def clear_fill():
    display.clear()
    display.fill_rectangle(0,0, 239,319, drk_grn)
            
        
def get_score():
        
        """ Determine home or away from Team Ids Data """
        home_id = games[0].get("home_id",'NA')
        away_id = games[0].get("away_id",'NA')
        
        import ujson
        with open("/mlbapp/team_ids.py") as f:
            all_teams = f.read()
        all_team_ids = ujson.loads(all_teams)
        
        team1 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == home_id][0]).upper()
        team2 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == away_id][0]).upper()
        
        """ typical 'x' above
        ...
         "teams" : [ {
            "id" : 133,
            "name" : "Oakland Athletics",
            "teamCode" : "oak",
            "fileCode" : "oak",
            "teamName" : "Athletics",
            "locationName" : "Oakland",
            "shortName" : "Oakland"
          }
        ...
        """
        
        global our_score
        global opp_score
        if team_id == home_id:
            print('We are the home team')
            our_score  = team1_score = games[0].get("home_score",'NA')
            opp_score  = team2_score = games[0].get("away_score",'NA')
        else:
            print('We are the away team')
            our_score  = team2_score = games[0].get("away_score",'NA')
            opp_score  = team1_score = games[0].get("home_score",'NA')
        
                    
        """ Records """
        home_rec = games[0].get('home_rec','NA')
        away_rec = games[0].get('away_rec','NA')
        
        """ Statuses
            "In Progress"
            "Umpire Review"?
            "Scheduled"
            "Pre-Game"
            "Warmup"
            "Final"
            "Game Over"
            "Delayed"
        """

        """ Status Check """
        game_status = games[0].get("status",'NA')
        if game_status == "In Progress" or "eview" in game_status:
            
            balls   = games[0].get('Balls','NA')
            strks   = games[0].get('Strikes','NA')
            outs    = games[0].get('Outs','NA')	
            inn_cur = games[0].get("current_inning",'NA')
            in_sta  = games[0].get("inning_state",'NA')[:3]
            batter  = get_x_p(games[0].get("Batter",'NA'))
                    
            clear_fill()
            display.draw_text(0,  start + (0 * delta), f"{mt}-{dy} {in_sta} {inn_cur}", date_font,  white , drk_grn)
            display.draw_text(5,  start + (1 * delta) + 5, f"{team1}:{team1_score} H {home_rec}", score_font, white , drk_grn)
            display.draw_text(5,  start + (2 * delta) + 5, f"{team2}:{team2_score} A {away_rec}", score_font, white , drk_grn)
            display.draw_text(5,  start + (3 * delta) + 5, f"AB: {batter}"                      , sm_font,    white , drk_grn)
            display.draw_text(10, start + (4 * delta) + 5, f"B: {balls} S: {strks} O: {outs }"  , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 60 * 1# check back every 2 minutes
        
        elif game_status == "Game Over" or game_status == "Final":
            
            lp = get_x_p(games[0]['losing_pitcher'])
            wp = get_x_p(games[0]['winning_pitcher'])
            
            clear_fill()
            display.draw_text(0, start + (0 * delta), f"{mt}-{dy} Final" , date_font,  white , drk_grn)
            display.draw_text(5, start + (1 * delta), f"{team1}:{team1_score} H {home_rec}" , score_font, white , drk_grn)
            display.draw_text(5, start + (2 * delta), f"{team2}:{team2_score} A {away_rec}" , score_font, white , drk_grn)
            display.draw_text(5, start + ((3 * delta) + 4), f"WP: {wp}"                           , sm_font,    white , drk_grn)
            display.draw_text(5, start + (4 * delta), f"LP: {lp}"                           , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 60 * 60 *4 # check back 4 hours from now
        
        else:  #"Scheduled"/"Warm up"/"Pre Game"

            gm_time=games[0].get('game_datetime','NA')
            tm=utc_to_local(gm_time)
            hour=tm.split(' ')[1]
            
            clear_fill()
            display.draw_text(0, start + (0 * delta), f"{mt}-{dy} {game_status}"   , date_font,  white , drk_grn)
            display.draw_text(5, start + (1 * delta), f"{team1} H {home_rec}"   , score_font, white , drk_grn)
            display.draw_text(5, start + (2 * delta), f"{team2} A {away_rec}"   , score_font, white , drk_grn)
            display.draw_text(5, start + (3 * delta), f"Game at {hour}" , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 60 * 20 # check back every 20 minutes
        

def no_gm():
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    clear_fill()
    draw_outline_box()
    display.draw_text(5, 5, gm_dt, date_font, white, drk_grn)
    display.draw_text(5, 75, 'No Game Today!', date_font, white, drk_grn)
    print(f"No Game today!")
    
while True:
    
    print(f"Version: {version}")
    import gc
    gc.collect()
    yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
    short_yr = f"{int( str(yr)[2:]):02d}"
    gm_dt = f"{mt}/{dy}/{yr}"
    print("Date: ",gm_dt)
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}

    try:
        games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
    except OSError as e:
        #Catch this known weird, unrecoverable issue and reboot
        #https://github.com/espressif/esp-idf/issues/2907
        if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
            import machine
            machine.reset()
    else:
        if not games:
            no_gm()
            time.sleep(60 * 240)  # check back 4 hours from now
        else:
            print(games[0])
            what_sleep=get_score()
            print(f"Sleeping {what_sleep} seconds")
            time.sleep(what_sleep)           