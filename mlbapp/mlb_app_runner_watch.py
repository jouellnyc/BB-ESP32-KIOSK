""" OLED SETUP """
#All drivers and fonts from https://github.com/russhughes/st7789_mpy
import st7789
from  hardware.lilygo_watch_tft_config  import config as tft_config
import fonts.lily_go_watch_vga1_bold_16x32 as date_font

tft = tft_config(rotation=90)
tft.init()

score_font = date_font
sm_font = date_font
drk_grn = st7789.color565(50,100,30)
white   =  st7789.WHITE

def draw_outline_box():
    tft.hline(  0,   0, 239, white)
    tft.hline(  0, 239, 239, white)
    tft.hline(  0,  50, 239, white)
    tft.vline(  0,   0, 239, white)
    tft.vline(  0, 239, 239, white)

def print_setup(text):
    tft.text(font,text,25,25, white, st7789.RED)

def clear_fill():
    tft.fill(drk_grn)

class Watch:
    
    def draw_text(self, startx, starty, text, font, fg_text, bg_text):
         tft.text(font, text, startx, starty, st7789.WHITE, drk_grn)
    
display = Watch()


import sys
import time

""" All non caught errors are handled by main.py """  
from . team_id import team_id
start=5 
delta=45

""" MLB SETUP """
from . import my_mlb_api
from hardware.ntp_setup import utc_to_local
url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    
""" Version """
from .version import version
   
def get_start_date(url, ua):
    import re
    import mrequests
    t=mrequests.get(url, headers={"User-Agent" : ua})
    _mtch= re.search("scheduled to begin on\s+([A-Z][a-z]+\s+[0-9]+)",t.text)
    print(f"m1 {_mtch}")
    if _mtch:
        try:
            start_date = _mtch.group(1)
        except IndexError as e:
            start_date = "??"
        finally:
            print(start_date)
            return start_date

def say_fetching():
    clear_fill()
    draw_outline_box()
    display.draw_text(5, 5,'Fetching Data',date_font, white, drk_grn)

def days_til_open():
    say_fetching()
    start_date=get_start_date(url, ua)
    clear_fill()
    draw_outline_box()
    display.draw_text(5,  start + (0 * delta)     ,f"{mt}-{dy}-{short_yr}", date_font,  white , drk_grn)
    display.draw_text(5,  start + (1 * delta) + 5 ,f"Opening"             , score_font, white , drk_grn)
    display.draw_text(5,  start + (2 * delta) + 5 ,f"Day is"              , score_font, white , drk_grn)
    display.draw_text(5,  start + (3 * delta) + 5 ,f"{start_date}"        , score_font, white , drk_grn)

def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

def no_gm():
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    clear_fill()
    draw_outline_box()
    display.draw_text(5, 5, gm_dt, date_font, white, drk_grn)
    display.draw_text(5, 75, 'No Game Today!', date_font, white, drk_grn)
    print(f"No Game today!")
    
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
        
        """ Statuses are one of:
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
            in_sta  = games[0].get("inning_state",'NA')
            batter  = get_x_p(games[0].get("Batter",'NA'))
                    
            clear_fill()
            display.draw_text(0,  start + (0 * delta), f"{mt}-{dy}-{short_yr} {in_sta} {inn_cur}", date_font,  white , drk_grn)
            display.draw_text(5,  start + (1 * delta) + 5, f"{team1}:{team1_score} H {home_rec}" , score_font, white , drk_grn)
            display.draw_text(5,  start + (2 * delta) + 5, f"{team2}:{team2_score} A {away_rec}" , score_font, white , drk_grn)
            display.draw_text(5,  start + (3 * delta) + 5, f"AB: {batter}"                       , sm_font,    white , drk_grn)
            display.draw_text(10, start + (4 * delta) + 5, f"B: {balls} S: {strks} O: {outs }"   , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 5
            return 60 * 1# check back every 2 minutes
        
        elif game_status == "Game Over" or game_status == "Final":
            
            lp = get_x_p(games[0]['losing_pitcher'])
            wp = get_x_p(games[0]['winning_pitcher'])
            
            clear_fill()
            display.draw_text(0, start + (0 * delta), f"{mt}-{dy}-{short_yr} {game_status}" , date_font,  white , drk_grn)
            display.draw_text(5, start + (1 * delta), f"{team1}:{team1_score} H {home_rec}" , score_font, white , drk_grn)
            display.draw_text(5, start + (2 * delta), f"{team2}:{team2_score} A {away_rec}" , score_font, white , drk_grn)
            display.draw_text(5, start + (3 * delta), f"WP: {wp}"                           , sm_font,    white , drk_grn)
            display.draw_text(5, start + (4 * delta), f"LP: {lp}"                           , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 5
            return 60 * 60 *4 # check back 4 hours from now
        
        else:  #"Scheduled"/"Warm up"/"Pre Game"
            
            gm_time=games[0].get('game_datetime','NA')
            tm=utc_to_local(gm_time)
            
            clear_fill()
            display.draw_text(0, start + (0 * delta), f"{mt}-{dy}-{short_yr} {game_status}" , date_font, white , drk_grn)
            display.draw_text(5, start + (1 * delta), f"{team1} H {home_rec}"               , score_font, white , drk_grn)
            display.draw_text(5, start + (2 * delta), f"{team2} A {away_rec}"               , score_font, white , drk_grn)
            display.draw_text(5, start + (3 * delta), f"Game at {tm}"                       , sm_font,    white , drk_grn)
            draw_outline_box()
            
            return 5
            return 60 * 20 # check back every 20 minutes
        

while True:
    
    factory_test = "True"
    import gc
    gc.collect()
    
    print(f"Version: {version}")
    yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
    short_yr = f"{int( str(yr)[2:]):02d}"
    gm_dt = f"{mt}/{dy}/{yr}"
    print("Date: ",gm_dt)
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    print("Month is",mt)
    
    if int(mt) in [09,10,11,12,01,02,03]:
        
        days_til_open()
        time.sleep(60 * 60 * 24 ) # check back Tommorow
        
    else:
        
        if factory_test == "True":
            from .games import games
        
        for x in games:
            
            try:
                #from .games import games
                #games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
                games = [x]
            except OSError as e:
                #Catch this known weird, unrecoverable issue and reboot
                #https://github.com/espressif/esp-idf/issues/2907
                if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
                    import machine
                    machine.reset()
            else:
                if not games:
                    no_gm()
                    time.sleep(60 * 60 * 4)  # check back 4 hours from now
                else:
                    print(games[0])
                    what_sleep=get_score()
                    print(f"Sleeping {what_sleep} seconds")
                    time.sleep(what_sleep) 

