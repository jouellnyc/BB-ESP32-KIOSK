import os
import sys
import utime
import time
import mrequests as requests
import ujson
from .news import News

""" SCREEN SETUP """ 
from hardware.screen_runner import display as d

""" All non caught errors are handled by main.py """  
from bbapp.team_id import team_id, team_name, team_code
from bbapp.team_colors import TEAM_COLORS
from hardware.ili9341 import color565
start=5 
delta=45

""" BB SETUP """
from . import my_mlb_api
od_url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
opening_day = 'March 30'
news_url="https://www.mlb.com/news/"

""" Version """
from .version import version

def set_team_color():
    global your_team_color
    r, g, b = TEAM_COLORS[team_code.upper()]
    your_team_color = color565(r, g, b)

def check_if_game(sleep=7):
    print("Checking if there's a game") if DEBUG else None
    if not games:
        no_gm()
    else:
        print(f"== Game: {games[0]}")
        print(f"Status: {games[0]['status']}")
        what_sleep=get_score()
        print(f"  Sleeping {what_sleep} seconds in check_if_game") if DEBUG else None
        time.sleep(what_sleep)         

def check_season():
    print("start check_season") if DEBUG else None
    if (int(mt) in [04, 05, 06, 07, 08, 09, 10]) or \
       (int(mt) == 3 and (int(dy) == 30 or int(dy) == 31)):
        print("Regular Season") 
        reg_season()
        check_if_game()
    else:
        print("Off Season")
        off_season()

def clear_story_area():
    d.fill_rectangle(1, 41, 318, 198, d.drk_grn)
    
def cycle_stories(func, news=0, func_sleep=30):
    print('Now in cycle_stories') if DEBUG else None
    story_count=1 ;
    if test_regular_season:
        story_sleep=1
    else:
        story_sleep=7
    for story in news:
        print(f"== {story_count}")
        if story_count > 0 and story_count % 7 == 0:
            func()
            print(f"Sleeping for {func_sleep} in cycle stories for {func.__name__}") if DEBUG else None
            time.sleep(func_sleep)
            clear_story_area()
        else:
            d.draw_text(5, start + (0 * delta), f"MLB News: {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
            """ Díaz - í is not supported by the font, make it a simple 'i' """
            story = rm_accents(story)
            d.draw_text(42, 215, "Story at mlb.com", d.sm_font,  d.white , d.drk_grn)
            d.scroll_print(text=story, y_pos=60, x_pos=18,
                           scr_len=18, clear=False, font=d.date_font,
                           bg=d.drk_grn, fg=d.white)
            """ x_pos for fill_rectangle must be at 1     """
            """ to keep vert lines from being overwritten """
            print(f"Sleeping for {story_sleep} in cycle stories_else {__name__}") if DEBUG else None
            time.sleep(story_sleep)
            clear_story_area()
        story_count+=1
        
def get_all_team_ids():
    with open("/bbapp/team_ids.py") as f:
        return ujson.loads(f.read())
        
def get_score():
        print("start get_score") if DEBUG else None
        """ Determine home or away from Team Ids Data """
        home_id = games[0].get("home_id",'NA')
        away_id = games[0].get("away_id",'NA')
        
        
        all_team_ids = get_all_team_ids()
        
        global team1
        global team2
        global t1_color
        global t2_color
        
        team1 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == home_id][0]).upper()
        team2 = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == away_id][0]).upper()
        r, g, b = TEAM_COLORS[team1]
        t1_color = color565(r, g, b)
        r, g, b = TEAM_COLORS[team2]
        t2_color = color565(r, g, b)
        
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
        global team1_score
        global team2_score
        
        """ These are both strings - Reminder """
        if team_id == home_id:
            print('We are the home team')
            our_score  = team1_score = games[0].get("home_score",'NA')
            opp_score  = team2_score = games[0].get("away_score",'NA')
        else:
            print('We are the away team')
            our_score  = team2_score = games[0].get("away_score",'NA')
            opp_score  = team1_score = games[0].get("home_score",'NA')
        
                    
        """ Records """
        global home_rec
        global away_rec
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
        global game_status
        game_status = games[0].get("status",'NA')
        
        if game_status == "In Progress" or "eview" in game_status:
            
            balls   = games[0].get('Balls','NA')
            strks   = games[0].get('Strikes','NA')
            outs    = games[0].get('Outs','NA')	
            inn_cur = games[0].get("current_inning",'NA')
            ordinals = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 10: 'th'}
            in_sta  = games[0].get("inning_state",'NA')
            batter  = get_x_p(games[0].get("Batter",'NA'))
                    
            d.clear_fill()
            d.draw_text(5,  start + (0 * delta),     f"{in_sta} {inn_cur}{ordinals[inn_cur]} {mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
            d.draw_text(5,  start + (1 * delta) + 5, f"{team1}:{team1_score} H {home_rec}" , d.score_font, d.white , t1_color)
            d.draw_text(5,  start + (2 * delta) + 5, f"{team2}:{team2_score} A {away_rec}" , d.score_font, d.white , t2_color)
            d.draw_text(5,  start + (3 * delta) + 5, f"AB: {batter}"                       , d.sm_font,    d.white , d.drk_grn)
            d.draw_text(10, start + (4 * delta) + 5, f"B: {balls} S: {strks} O: {outs }"   , d.sm_font,    d.white , d.drk_grn)
            d.draw_outline_box()
            
            if test_regular_season:
                print("Testing Regular Season")
                return 2
            return 20 # check back every x seconds
        
        elif game_status == "Game Over" or game_status == "Final":
            
            """ Stretch the Game Status to minimize ghost pixelation """
            """ here and with ZZZ in Warm up  below                  """
            if test_regular_season:
                fsleep=5
            else:
                fsleep=30            
            show_final()
            print(f'sleeping for {fsleep} in  {game_status}') if DEBUG else None
            time.sleep(fsleep)
            show_filler_news(show_final, func_sleep=fsleep)
            return 1
        
        elif game_status == "Scheduled":
            if test_regular_season:
                fsleep=5
            else:
                fsleep=30            
            show_scheduled()
            print(f'sleeping for {fsleep} in  {game_status}') if DEBUG else None
            time.sleep(fsleep)
            show_filler_news(show_scheduled, func_sleep=fsleep)
            return 1
        
        else:  # Warm up"/"Pre Game / Delayed"
            show_scheduled()
            if test_regular_season:
                return 2
            return 60 * 10 # check back every 10 minutes
        
def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        
        
def no_gm(sleep=7):
    show_no_gm()
    print(f"Sleeping for {sleep} seconds in show_no_gm")
    time.sleep(sleep)
    show_filler_news(show_no_gm)    

def off_season(sleep=30):
    print("start off season") if DEBUG else None
    opening_day_screen()
    print(f"Sleeping for {sleep} seconds in off_season")
    time.sleep(sleep)
    gc.collect()
    show_filler_news(opening_day_screen)
    gc.collect()

def opening_day_screen():
    print("start opening_day_screen") if DEBUG else None
    d.fresh_box()
    show_logo()
    d.draw_text(5,    start + (0 * delta)      ,f"{mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
    d.draw_text(42,   start + (1 * delta) + 25 ,f"Opening Day"         , d.score_font, d.white , d.drk_grn)
    d.draw_text(127,  start + (2 * delta) + 25 ,f"is"                  , d.score_font, d.white , d.drk_grn)
    d.draw_text(65,   start + (3 * delta) + 25 ,f"{opening_day}"       , d.score_font, d.white , d.drk_grn)
    
def reg_season():
    global games
    games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
    
def regular_season_test():
    #If no game that day games will be empty, not undefined
    global games
    from .test_games import games
    print(f"Games {games}")
    for x in games:
        games = [x]
        check_if_game()
    games = []
    check_if_game()

def rm_accents(story):
    """ Replace Accent Accent aigu, grave, and unicode apostrophes """
    return story.replace('\xed','i').replace('\xe9','e').replace('\xc0','A')\
                .replace('\xe8','e').replace('\xec','i').replace('\xd2','O')\
                .replace('\xf9','u').replace('\xc9','E').replace('\xe1','a')\
                .replace('\xcd','I').replace('\xf3','o').replace('\xda','U')\
                .replace(u"\u2018", "'").replace(u"\u2019", "'")\
                .replace(u'\xa0', u' ').replace(u'\xc1','A')

def say_fetching(text='Fetching Data'):
    d.fresh_box()
    d.draw_text(5, 5, text, d.date_font, d.white, d.drk_grn)
   
def show_filler_news(func, func_sleep=30):
    print('In show_filler_news') if DEBUG else None
    say_fetching("Fetching News")
    news = n.get_latest_news()
    print(n.news)
    d.fresh_box()
    cycle_stories(func, news, func_sleep=30)

def show_final():
    game_status = "Final Score"
    lp = get_x_p(games[0]['losing_pitcher'])
    wp = get_x_p(games[0]['winning_pitcher'])
    d.clear_fill()
    d.draw_text(5, start + (0 * delta), f"{game_status} {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
    d.draw_text(5, start + (1 * delta), f"{team1}:{team1_score} H {home_rec}" , d.score_font, d.white , t1_color)
    d.draw_text(5, start + (2 * delta), f"{team2}:{team2_score} A {away_rec}" , d.score_font, d.white , t2_color)
    d.draw_text(5, start + (3 * delta), f"WP: {wp}"                           , d.sm_font,    d.white , t1_color)
    d.draw_text(5, 0     + (4 * delta), f"LP: {lp}"                           , d.sm_font,    d.white , t2_color)
    d.draw_outline_box()

def show_scheduled():
    gm_time=games[0].get('game_datetime','NA')
    """ Take the UTC Time in MLB Api and display it in the local timezone """
    tm=utc_to_local(gm_time)
    d.clear_fill()
    d.draw_text(5, start + (0 * delta), f"{game_status} {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
    d.draw_text(5, start + (1 * delta), f"{team1}:N H {home_rec}"             , d.score_font, d.white , t1_color)
    d.draw_text(5, start + (2 * delta), f"{team2}:N A {away_rec}"             , d.score_font, d.white , t2_color)
    d.draw_text(5, start + (3 * delta), f"Game at {tm}"                       , d.sm_font,    d.white , d.drk_grn)
    d.draw_text(5, start + (4 * delta), f"ZZZZZZZZZZZZZZZZZZZZZ"              , d.sm_font,   d.drk_grn, d.drk_grn)
    d.draw_outline_box()
    
    
def show_logo():
    print("start show_logo") if DEBUG else None
    d.draw_text(235, 5,  team_code.upper(), d.date_font, d.white, d.drk_grn)
    
def show_no_gm():
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    d.fresh_box()
    d.draw_text(5,   5,  gm_dt, d.date_font, d.white, d.drk_grn)
    show_logo()
    d.draw_text(40, 75,  f"No {team_name}" , d.score_font, d.white, your_team_color)
    d.draw_text(40, 125, f"Game Today!"    , d.score_font, d.white, your_team_color)
    


while True:
    
    DEBUG=True
    
    import gc
    gc.collect()
    
    global games
    force_offseason = False
    test_regular_season = False
    set_team_color()
    
    print(f"Version: {version}")
    from hardware.ntp_setup import utc_to_local, timezone
    yr, mt, dy, hr, mn, s1, s2, s3 = [  f"{x:02d}" for x in utime.localtime(utime.mktime(utime.localtime()) + (int(timezone)*3600)) ]
    """ Game Time to query  MLB API for game data using timezone in ntp_setup.py """
    gm_dt = f"{mt}/{dy}/{yr}"
    print(f"Today's Local Game Date: {gm_dt}")
    short_yr = f"{int( str(yr)[2:]):02d}"
    news_file = f"news.{mt}-{dy}-{yr}.txt"
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    n = News(news_file)
 
    try:
        if force_offseason:
            #Will go on infinitely ...
            off_season()
        elif test_regular_season:
            #Will go on infinitely ...
            regular_season_test()
        else:
            check_season()        
    except OSError as e:
        #Catch this known weird, unrecoverable issue and reboot
        #https://github.com/espressif/esp-idf/issues/2907
        if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
            import machine
            machine.reset()