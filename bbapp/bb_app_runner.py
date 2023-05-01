import os
import sys
import utime
import time
import urequests
import ujson

""" All non caught errors are handled by main.py """  

""" SCREEN SETUP """ 
from hardware.screen_runner import display as d

""" Imports """
from bbapp.team_id import team_id, team_name, team_code
from bbapp.team_colors import TEAM_COLORS
from hardware.ili9341 import color565
from hardware.ntp_setup import utc_to_local, timezone, tz_name
from . import my_mlb_api
from .news import News
""" Version """
from .version import version

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"    >>  {func.__name__} start")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"    << {func.__name__} = Elapsed time: {elapsed_time:.2f} seconds")
        return result
    return wrapper

        
@timing_decorator        
def check_season():
    if (int(mt) in [04, 05, 06, 07, 08, 09, 10]) or \
       (int(mt) == 3 and (int(dy) == 30 or int(dy) == 31)):
        print("It's the Regular Season") 
        reg_season()
    else:
        print("Off Season")
        off_season()

@timing_decorator
def reg_season():
    check_if_game()
    
def check_if_game():
    get_todays_games()
    if not games:
        no_gm()
    else:
        show_gm(sleep=7)

@timing_decorator
def get_todays_games():
    global games
    global game_id
    print("Connecting to MLB live sched data") if DEBUG else None
    games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
    if len(games) > 1:
        print("More that one game Today!")
        if games[0]['status'] == "Final":
            games[0]=games[1]
    game_id=games[0].get('game_id','NA')

def show_gm(sleep=7):
    print(f"> Game: {games[0]}")
    print(f"Status: {games[0]['status']}")
    set_teams()
    what_sleep=get_score()
    print(f" Sleeping {what_sleep} seconds after get_score") if DEBUG else None
    time.sleep(what_sleep)

def set_teams():
    set_team_records()
    set_team_ids()
    set_team_colors()

def set_team_records():
    """ Records """
    global home_rec
    global away_rec
    home_rec = games[0].get('home_rec','NA')
    away_rec = games[0].get('away_rec','NA')
    
def set_team_ids():
    global home_id
    global away_id
    """ Determine home or away from Team Ids Data """
    home_id = games[0].get("home_id",'NA')
    away_id = games[0].get("away_id",'NA')
    """ These are both strings - Reminder """
    if team_id == home_id:
        print('Who: We are the home team')
    else:
        print('We are the away team')
    
def set_team_colors():
    global home_team
    global away_team
    global home_team_color
    global away_team_color
    home_team = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == home_id][0]).upper()
    away_team = str([x["teamCode"] for x in all_team_ids["teams"] if x["id"] == away_id][0]).upper()
    r, g, b = TEAM_COLORS[home_team]
    home_team_color = color565(r, g, b)
    r, g, b = TEAM_COLORS[away_team]
    away_team_color = color565(r, g, b)
        
    
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

def gc_status_flush():
    print("Mem: ", gc.mem_free()) if MEM_DEBUG else None
    gc.collect()
    print("Mem: ", gc.mem_free()) if MEM_DEBUG else None
            
def get_all_team_ids():
    with open("/bbapp/team_ids.py") as f:
        return ujson.loads(f.read())

@timing_decorator
def get_current_play_data():
    url=f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live?fields=gamePk,liveData,plays,currentPlay,result,description,awayScore,homeScore,about,batter,count,inning,halfInning,balls,strikes,outs,matchup,postOnFirst,postOnSecond,postOnThird,fullName,gameData,status,detailedState,decisions,winner,loser"
    print(f"Connecting to MLB live data at {url}") if DEBUG else None
    return ujson.loads(urequests.get(url).text)
    ####return { 'postOnFirst': {'fullName' :'Frank Smithers'},  'postOnSecond':  {'fullName' :'Samual Hdithers'}, 'postOnThird':  {'fullName' :'Theodore Thumb'} }
   
                                               
def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    print("pname", pname) if DEBUG else None
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

@timing_decorator
def get_score():

    global current_play_data
    current_play_data=get_current_play_data()
    print('current_play_data',current_play_data)
    gc_status_flush()
    
    """ Status Check - Statuses are one of:
        "In Progress"
        "Umpire Review"?
        "Scheduled"
        "Pre-Game"
        "Warmup"
        "Final"
        "Game Over"
        "Delayed"
        "Manager challenge: XXX"
                                        """
    global game_status
    game_status = current_play_data['gameData']['status']['detailedState']
    ###game_status = "In Progress"
    
    
    if (game_status == "In Progress")  or (( "eview" or "challenge" ) in game_status):

        currentPlay = current_play_data['liveData']['plays']['currentPlay']
        
        global away_score
        global home_score
        away_score   = currentPlay['result']['awayScore']
        home_score   = currentPlay['result']['homeScore']
    
        global balls
        global strks
        global outs
        global inn_cur
        global in_sta
        global batter
        global up
        
        balls         = currentPlay['count']['balls']
        strks         = currentPlay['count']['strikes']
        outs          = currentPlay['count']['outs']
        inn_cur       = currentPlay['about']['inning']
        in_sta        = currentPlay['about']['halfInning']
        in_sta        = in_sta[0].upper() + in_sta[1:]
        batter        = get_x_p(currentPlay['matchup']['batter']['fullName'])
        
        d.clear_fill()
        
        if "Bottom" in in_sta:
            up=f"{home_team} up"
        elif "Top" in in_sta:
            up=f"{away_team} up"
        elif "End" or "Middle" in in_sta:
            up=f"{mt}-{dy}-{short_yr}"
        
        """ Show the Current Score """
        show_in_progress()
        in_progress_sleep=7
        print(f"sleeping {in_progress_sleep} after showing score/in_progress")
        time.sleep(in_progress_sleep)
        gc_status_flush()
        
        """ Check the Current play vs Previous Play """
        global previous_play
        """ current_play_index may or may not have 'result' => 'description' """
        """ allPlays'][current_play_index] may have it's 'result' => 'description' updated from the 'current' to the final one """
        cur_play  = current_play_data['liveData']['plays']['currentPlay'].get('result', {}).get('description')
        
        print(f"cur_play {cur_play} previous_play {previous_play}") if DEBUG else None
        
        if cur_play is not None:
            if cur_play != previous_play:
                print(f"Play change: {cur_play}")
                previous_play = cur_play
                d.fresh_box()
                d.draw_text(5,  start + (0 * delta), f"{in_sta} {inn_cur}{ordinals[inn_cur]} {mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
                d.scroll_print(text=cur_play, y_pos=60, x_pos=18,
                               scr_len=18, clear=False, font=d.date_font,
                               bg=d.drk_grn, fg=d.white)
            else:
                print(f"Play change: No")
        else:
            print("Play is None")
            
        play_check_sleep=5
        print(f"Sleeping {play_check_sleep} after Current Play Check/Show")
        time.sleep(play_check_sleep)
        gc_status_flush()
                    
        
        """ Now, Check Runners """
        runners       = current_play_data['liveData']['plays']['currentPlay']['matchup']
        if runners_changed(runners):
            print('Runners Changed')
            show_runners(runners)
        else:
            print('Runners Did not Change')
        runners_sleep=5
        print(f"Sleeping {runners_sleep} after runners")
        time.sleep(runners_sleep)
        gc_status_flush()
            
        if test_regular_season:
            print("Testing Regular Season")
            return 2
        
        return 1 # Delay another check back for  x more  seconds
        
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
    
    
    elif game_status == "Warmup":
        show_scheduled()
        if test_regular_season:
            return 2
        return 60 * 2# check back every 2 minutes
    
    
    else:  #"Pre Game / Delayed"
        show_scheduled()
        if test_regular_season:
            return 2
        return 60 * 10 # check back every 10 minutes

def show_in_progress():
    print(f"balls:{balls} strikes:{strks} outs:{outs}")  if DEBUG else None
    print(f"{in_sta} {inn_cur}{ordinals[inn_cur]} {up}")           if DEBUG else None
    d.draw_text(5, start + (0 * delta),     f"{in_sta} {inn_cur}{ordinals[inn_cur]} {up}", d.date_font,  d.white , d.drk_grn)
    d.draw_text(5, start + (1 * delta) + 5, f"{home_team}:{away_score} H {home_rec}"   , d.score_font, d.white , home_team_color)
    d.draw_text(5, start + (2 * delta) + 5, f"{away_team}:{home_score} A {away_rec}"   , d.score_font, d.white , away_team_color)
    d.draw_text(5, start + (3 * delta) + 5, f"AB: {batter}"                         , d.sm_font,    d.white , d.drk_grn)
    d.draw_text(10,start + (4 * delta) + 5, f"B: {balls} S: {strks} O: {outs }"     , d.sm_font,    d.white , d.drk_grn)
    show_runners_front()
    d.draw_outline_box()
        
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

def runners_changed(runners):
    
    current_bases =  {}
    current_bases['1st']=runners.get('postOnFirst', {}).get('fullName')
    current_bases['2nd']=runners.get('postOnSecond', {}).get('fullName')
    current_bases['3rd']=runners.get('postOnThird' , {}).get('fullName')
    
    global bases
    print('Inside Checking for runners changed : bases: ',  bases) if DEBUG else None
    print('Inside Checking for runners changed : current_bases:', current_bases) if DEBUG else None
    
    if current_bases != bases:
        bases = current_bases
        return True
    return False

def say_fetching(text='Fetching Data'):
    d.fresh_box()
    d.draw_text(5, 5, text, d.date_font, d.white, d.drk_grn)
   
def set_team_color():
    global your_team_color
    r, g, b = TEAM_COLORS[team_code.upper()]
    your_team_color = color565(r, g, b)

def show_filler_news(func, func_sleep=30):
    print('In show_filler_news') if DEBUG else None
    say_fetching("Fetching News")
    news = n.get_latest_news()
    print(n.news) if DEBUG else None
    d.fresh_box()
    cycle_stories(func, news, func_sleep=30)

def show_final():
    game_status = "Final Score"
    lp = get_x_p(current_play_data['liveData']['decisions']['winner']['fullName']) 
    wp = get_x_p(current_play_data['liveData']['decisions']['loser']['fullName'])
    d.clear_fill()
    d.draw_text(5, start + (0 * delta), f"{game_status} {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
    d.draw_text(5, start + (1 * delta), f"{home_team}:{home_score} H {home_rec}" , d.score_font, d.white , home_team_color)
    d.draw_text(5, start + (2 * delta), f"{away_team}:{away_score} A {away_rec}" , d.score_font, d.white , away_team_color)
    d.draw_text(5, start + (3 * delta), f"WP: {wp}"                           , d.sm_font,    d.white , home_team_color)
    d.draw_text(5, 0     + (4 * delta), f"LP: {lp}"                           , d.sm_font,    d.white , away_team_color)
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

def show_runners_front():

    def onbase():
        d.fill_polygon(ax, bx, cx, dx, d.white, rotate=0)

    def empty():
        d.draw_polygon(ax, bx, cx, dx, d.white, rotate=0)

    ax=4; bx=275; cx=200; dx=10
    if bases['1st']:
        onbase()
    else:
        empty()
        
    ax=4; bx=250; cx=165; dx=10
    if bases['2nd']:
        onbase()
    else:
        empty()
        
    ax=4; bx=225; cx=200; dx=10   
    if bases['3rd']:
        onbase()
    else:
        empty()


def show_runners(runners):
    
    
    def onbase():
        d.fill_polygon(ax, bx, cx, dx, d.white, rotate=0)

    def empty():
        d.draw_polygon(ax, bx, cx, dx, d.white, rotate=0)

    d.clear_fill()
    d.draw_outline_box()
    d.draw_text(5,  start + (0 * delta), f"{in_sta} {inn_cur}{ordinals[inn_cur]} {mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
            
    fn='fullName'
    what='postOnFirst'
    print('Show Runners bases ',bases)
    ax=4; bx=215; cx=150; dx=15
    if bases['1st']:
        d.draw_text(195, 180, get_x_p(bases['1st']), d.sm_font,    d.white , d.drk_grn) 
        onbase()
        
    else:
        empty()
    
    ax=4; bx=155; cx=75; dx=15
    if bases['2nd']:
        onbase()
        d.draw_text( 95, 100, get_x_p(bases['2nd']), d.sm_font,    d.white , d.drk_grn)
    else:
        empty()
    
    ax=4; bx=95; cx=150; dx=15
    if bases['3rd']:
        onbase()
        d.draw_text(  2, 180, get_x_p(bases['3rd']), d.sm_font,    d.white , d.drk_grn)
        
    else:
        empty()

def show_scheduled():
    gm_time=games[0].get('game_datetime','NA')
    """ Take the UTC Time in MLB Api and display it in the local timezone """
    tm=utc_to_local(gm_time)
    d.clear_fill()
    d.draw_text(5, start + (0 * delta), f"{game_status} {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
    d.draw_text(5, start + (1 * delta), f"{home_team}:N H {home_rec}"             , d.score_font, d.white , home_team_color)
    d.draw_text(5, start + (2 * delta), f"{away_team}:N A {away_rec}"             , d.score_font, d.white , away_team_color)
    d.draw_text(5, start + (3 * delta), f"Game at {tm} {tz_name}"             , d.sm_font,    d.white , d.drk_grn)
    d.draw_text(5, start + (4 * delta), f"ZZZZZZZZZZZZZZZZZZZZZ"              , d.sm_font,   d.drk_grn, d.drk_grn)
    d.draw_outline_box()

""" Constants """
od_url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
opening_day = 'March 30'
news_url="https://www.mlb.com/news/"
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
ordinals      = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 10: 'th', 11: 'th', 12:'th'}
http_headers= { 'User-Agent': ua }
start=5 
delta=45

""" Debug Options """
force_offseason = False
test_regular_season = False
DEBUG = True
MEM_DEBUG = True

""" Globals """
bases = {'1st':None, '2nd': None, '3rd':None}
previous_play  = None

all_team_ids = get_all_team_ids()
set_team_color()
            
while True:
    
    import gc
    gc.collect()
    
    print(f"==== Version: {version}")
    
    """ Game Time to query  MLB API for game data using timezone in ntp_setup.py """
    yr, mt, dy, hr, mn, *_ = [  f"{x:02d}" for x in utime.localtime(utime.mktime(utime.localtime()) + (int(timezone)*3600)) ]
    gm_dt = f"{mt}/{dy}/{yr}"
    short_yr = f"{int( str(yr)[2:]):02d}"
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    print(f"Today's Local Game Date: {gm_dt}")
    
    news_file = f"news.{mt}-{dy}-{yr}.txt"
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