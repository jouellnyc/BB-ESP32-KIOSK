import os
import sys
import time
import re
import mrequests
    
""" SCREEN SETUP """ 
from hardware.screen_runner import display as d

""" All non caught errors are handled by main.py """  
from . team_id import team_id, team_name, team_code
start=5 
delta=45

""" BB SETUP """
from . import my_mlb_api
from hardware.ntp_setup import utc_to_local
od_url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
opening_day = 'March 30'
news_url="https://www.mlb.com/newsQ/"

""" Version """
from .version import version

class HTTPErr(Exception):
    pass

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
    if int(mt) in [11,12,01,02,03]:
        if int(mt) == 3 and int(dy) == 30:
            print("Regular Season") 
            reg_season()
            check_if_game()
        else:
            print("Off Season")
            off_season()
    else:
        print("Regular Season")
        reg_season()
        check_if_game()

def check_http_code(request):
    
    if request.status_code != 200:
        err=f"Request failed: {request.status_code} at {news_url}"
        print(err)
        count+=1
        time.sleep(5)
        get_latest_news(count=count, err=err)
    else:
        cleanup_news_files(request)
            
            
def cleanup_news_files(request):
    
    if save_news_file(request):
        
        print(f"News save to {news_file} OK")

        if rm_old_news():
            print("old news deleted OK")
        else:
            print("old news delete failed")
    else:
        print(f"News save to {news_file} failed")

def clear_story_area():
    d.fill_rectangle(1, 41, 318, 198, d.drk_grn)
    
def cycle_stories(func, func_sleep=30):
    print('Now in cycle_stories') if DEBUG else None
    story_count=1 ; story_sleep=7
    for story in news:
        print(f"== {story_count}")
        if story_count > 0 and story_count % 7 == 0:
            func()
            print(f"Sleeping for {story_sleep} in after {func.__name__}") if DEBUG else None
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
            print(f"Sleeping for {story_sleep} in {__name__}") if DEBUG else None
            time.sleep(story_sleep)
            clear_story_area()
        story_count+=1
        
def get_latest_news(count=1, err="reboot/netfail"):
    
    if count == 3:
        d.crash_burn(err)
    try:
        request = mrequests.get(news_url,headers={b"accept": b"text/html"})
    except OSError:
        print(f"Request failed. count: {count}")
        count+=1
        get_latest_news(count=count)
    else:
        check_http_code(request)


def get_news_from_file():
    global news
    news=[]
    try:
        with open(news_file) as fh:
            for line in fh:
                story = re.search('data-headline="(.*?)"',line)
                if story is not None:
                    news.append(story.group(1))
        print('Get news from file len', len(news)) if DEBUG else None
    except OSError:
        return ["Fail to get new news"]
    return news


def get_open_day():
    print('od_sf')
    say_fetching()
    print('od_gs')
    get_start_date(od_url, ua)

def get_score():
        
        """ Determine home or away from Team Ids Data """
        home_id = games[0].get("home_id",'NA')
        away_id = games[0].get("away_id",'NA')
        
        import ujson
        with open("/bbapp/team_ids.py") as f:
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
                    
            d.clear_fill()
            d.draw_text(5,  start + (0 * delta), f"{mt}-{dy}-{short_yr} {in_sta} {inn_cur}", d.date_font,  d.white , d.drk_grn)
            d.draw_text(5,  start + (1 * delta) + 5, f"{team1}:{team1_score} H {home_rec}" , d.score_font, d.white , d.drk_grn)
            d.draw_text(5,  start + (2 * delta) + 5, f"{team2}:{team2_score} A {away_rec}" , d.score_font, d.white , d.drk_grn)
            d.draw_text(5,  start + (3 * delta) + 5, f"AB: {batter}"                       , d.sm_font,    d.white , d.drk_grn)
            d.draw_text(10, start + (4 * delta) + 5, f"B: {balls} S: {strks} O: {outs }"   , d.sm_font,    d.white , d.drk_grn)
            d.draw_outline_box()
            
            if factory_test:
                return 2
            return 60 # check back every x minutes
        
        elif game_status == "Game Over" or game_status == "Final":
            
            """ Stretch the Game Status to minimize ghost pixelation """
            """ here and with ZZZ in Warm up  below                  """
            if factory_test:
                fsleep=5
            else:
                fsleep=30            
            def show_final():
                game_status = "Final Score"
                lp = get_x_p(games[0]['losing_pitcher'])
                wp = get_x_p(games[0]['winning_pitcher'])
                d.clear_fill()
                d.draw_text(5, start + (0 * delta), f"{mt}-{dy}-{short_yr} {game_status}" , d.date_font,  d.white , d.drk_grn)
                d.draw_text(5, start + (1 * delta), f"{team1}:{team1_score} H {home_rec}" , d.score_font, d.white , d.drk_grn)
                d.draw_text(5, start + (2 * delta), f"{team2}:{team2_score} A {away_rec}" , d.score_font, d.white , d.drk_grn)
                d.draw_text(5, start + (3 * delta), f"WP: {wp}"                           , d.sm_font,    d.white , d.drk_grn)
                d.draw_text(5, 0     + (4 * delta), f"LP: {lp}"                           , d.sm_font,    d.white , d.drk_grn)
                d.draw_outline_box()
            show_final()
            time.sleep(fsleep)
            show_filler_news(show_final, func_sleep=fsleep)
            return 1
        
        else:  #"Scheduled"/"Warm up"/"Pre Game"
            
            gm_time=games[0].get('game_datetime','NA')
            tm=utc_to_local(gm_time)
            
            d.clear_fill()
            d.draw_text(5, start + (0 * delta), f"{mt}-{dy}-{short_yr} {game_status}" , d.date_font,  d.white , d.drk_grn)
            d.draw_text(5, start + (1 * delta), f"{team1}:N H {home_rec}"             , d.score_font, d.white , d.drk_grn)
            d.draw_text(5, start + (2 * delta), f"{team2}:N A {away_rec}"             , d.score_font, d.white , d.drk_grn)
            d.draw_text(5, start + (3 * delta), f"Game at {tm}"                       , d.sm_font,    d.white , d.drk_grn)
            d.draw_text(5, start + (4 * delta), f"ZZZZZZZZZZZZZZZZZZZZZ"              , d.sm_font,   d.drk_grn, d.drk_grn)
            d.draw_outline_box()
            if factory_test:
                return 2
            return 60 * 10 # check back every 10 minutes
        
def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

        
def news_is_current():
    try:
        if os.stat(news_file):
            return True
    except OSError:
        return False

def no_gm(sleep=7):
    show_no_gm()
    print(f"Sleeping for {sleep} seconds in show_no_gm")
    time.sleep(sleep)
    show_filler_news(show_no_gm)    

def opening_day_screen():
    d.fresh_box()
    show_logo()
    d.draw_text(5,    start + (0 * delta)      ,f"{mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
    d.draw_text(42,   start + (1 * delta) + 25 ,f"Opening Day"         , d.score_font, d.white , d.drk_grn)
    d.draw_text(127,  start + (2 * delta) + 25 ,f"is"                  , d.score_font, d.white , d.drk_grn)
    d.draw_text(65,   start + (3 * delta) + 25 ,f"{opening_day}"        , d.score_font, d.white , d.drk_grn)
    
def off_season():
    opening_day_screen()
    gc.collect()
    show_filler_news(opening_day_screen)
    gc.collect()
    
def reg_season():
    global games
    games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
    """ games  = [   {'game_id': 663188, 'away_pitcher_note': '',
                            'winning_pitcher': 'Kyle Wright',
                            'winning_team': 'Atlanta Braves',
                                 'home_probable_pitcher': '',
                                   'game_date': '2022-08-10',
                                             'away_score': 8,
                                 'venue_name': 'Fenway Park',
                  'summary': '2022-08-10 - Atlanta Braves (8) @ Boston Red Sox (4) (Final)',
                  'home_rec': '54-58',
                  'inning_state': 'Bottom',
                  'status': 'In Progress',
                  # 'status': 'Pre Game',
                  #'status' : 'Game Over',
                  # 'status': 'Final',
                  'home_score': 4,
                  'save_pitcher': None,
                  'Balls'   : 1,
                  'Strikes' : 0,
                  'Outs'     :2 ,
                  'game_num': 1, 'away_name': 'Atlanta Braves', 'game_datetime': '2022-08-10T23:10:00Z',
                  'doubleheader': 'N', 'losing_team': 'Boston Red Sox', 'home_pitcher_note': '',
                  'away_probable_pitcher': '', 'game_type': 'R', 'home_name': 'Boston Red Sox',
                  'away_id': 144, 'current_inning': 9, 'home_id': 111, 'losing_pitcher': 'Nick Pivetta',
                  'Batter': 'James Heehan',
                  'current_inning' : 7,
                  'venue_id': 3, 'away_rec': '66-46'},
                              {'game_id': 663188, 'away_pitcher_note': '',
                            'winning_pitcher': 'Kyle Wright',
                            'winning_team': 'Atlanta Braves',
                                 'home_probable_pitcher': '',
                                   'game_date': '2022-08-10',
                                             'away_score': 8,
                                 'venue_name': 'Fenway Park',
                  'summary': '2022-08-10 - Atlanta Braves (8) @ Boston Red Sox (4) (Final)',
                  'home_rec': '54-58',
                  'inning_state': 'Bottom',
                   'status': 'Final',
                  'home_score': 4,
                  'save_pitcher': None,
                  'Balls'   : 1,
                  'Strikes' : 0,
                  'Outs'     :2 ,
                  'game_num': 1, 'away_name': 'Atlanta Braves', 'game_datetime': '2022-08-10T23:10:00Z',
                  'doubleheader': 'N', 'losing_team': 'Boston Red Sox', 'home_pitcher_note': '',
                  'away_probable_pitcher': '', 'game_type': 'R', 'home_name': 'Boston Red Sox',
                  'away_id': 144, 'current_inning': 9, 'home_id': 111, 'losing_pitcher': 'Nick Pivetta',
                  'Batter': 'James Heehan',
                  'current_inning' : 7,
                  'venue_id': 3, 'away_rec': '66-46'}]
    games = [ {'game_id': 663188, 'away_pitcher_note': '',
                            'winning_pitcher': 'Kyle Wright',
                            'winning_team': 'Atlanta Braves',
                                 'home_probable_pitcher': '',
                                   'game_date': '2022-08-10',
                                             'away_score': 8,
                                 'venue_name': 'Fenway Park',
                  'summary': '2022-08-10 - Atlanta Braves (8) @ Boston Red Sox (4) (Final)',
                  'home_rec': '54-58',
                  'inning_state': 'Bottom',
                  'status': 'Pre Game',
                  'home_score': 4,
                  'save_pitcher': None,
                  'Balls'   : 1,
                  'Strikes' : 0,
                  'Outs'     :2 ,
                  'game_num': 1, 'away_name': 'Atlanta Braves', 'game_datetime': '2022-08-10T23:10:00Z',
                  'doubleheader': 'N', 'losing_team': 'Boston Red Sox', 'home_pitcher_note': '',
                  'away_probable_pitcher': '', 'game_type': 'R', 'home_name': 'Boston Red Sox',
                  'away_id': 144, 'current_inning': 9, 'home_id': 111, 'losing_pitcher': 'Nick Pivetta',
                  'Batter': 'James Heehan',
                  'current_inning' : 7,
                  'venue_id': 3, 'away_rec': '66-46'}
              ]	
    
    games = [ {'game_id': 663188, 'away_pitcher_note': '',
                            'winning_pitcher': 'Kyle Wright',
                            'winning_team': 'Atlanta Braves',
                                 'home_probable_pitcher': '',
                                   'game_date': '2022-08-10',
                                             'away_score': 8,
                                 'venue_name': 'Fenway Park',
                  'summary': '2022-08-10 - Atlanta Braves (8) @ Boston Red Sox (4) (Final)',
                  'home_rec': '54-58',
                  'inning_state': 'Bottom',
                  'status' : 'Game Over',
                  'home_score': 4,
                  'save_pitcher': None,
                  'Balls'   : 1,
                  'Strikes' : 0,
                  'Outs'     :2 ,
                  'game_num': 1, 'away_name': 'Atlanta Braves', 'game_datetime': '2022-08-10T23:10:00Z',
                  'doubleheader': 'N', 'losing_team': 'Boston Red Sox', 'home_pitcher_note': '',
                  'away_probable_pitcher': '', 'game_type': 'R', 'home_name': 'Boston Red Sox',
                  'away_id': 144, 'current_inning': 9, 'home_id': 111, 'losing_pitcher': 'Nick Pivetta',
                  'Batter': 'James Heehan',
                  'current_inning' : 7,
                  'venue_id': 3, 'away_rec': '66-46'} ] """
    
def rm_accents(story):
    """ Replace Accent Accent aigu, grave, and unicode apostrophes """
    return story.replace('\xed','i').replace('\xe9','e').replace('\xc0','A')\
                .replace('\xe8','e').replace('\xec','i').replace('\xd2','O')\
                .replace('\xf9','u').replace('\xc9','E').replace('\xe1','a')\
                .replace('\xcd','I').replace('\xf3','o').replace('\xda','U')\
                .replace(u"\u2018", "'").replace(u"\u2019", "'")\
                .replace(u'\xa0', u' ')
def rm_old_news():
    try:
        [ os.unlink(x) for x in os.listdir() if 'news' in x and news_file not in x ]
    except OSError:
        return False
    else:
        return True

def run_factory_test():
    #If no game that day games will be empty, not undefined
    global games
    from .test_games import games
    print(f"Games {games}")
    for x in games:
        games = [x]
        check_if_game()
    games = []
    check_if_game()

def save_news_file(r):
    try:
        r.save(news_file)
    except OSError:
        raise
    else:
        return True

def say_fetching(text='Fetching Data'):
    d.fresh_box()
    d.draw_text(5, 5, text, d.date_font, d.white, d.drk_grn)
   
def show_filler_news(func, func_sleep=30):
    print('In show_filler_news') if DEBUG else None
    if factory_test or news_is_current():
        print('News is current - getting from file') if DEBUG else None
        say_fetching("Fetching News")
        get_news_from_file()
    else:
        print('News is old - actually getting news from the web')
        get_latest_news()
        say_fetching("Fetching News")
        get_news_from_file()
    d.fresh_box()
    cycle_stories(func, func_sleep=30)

def show_logo():
    d.draw_text(235, 5,  team_code.upper(), d.date_font, d.white, d.drk_grn)
    
def show_no_gm():
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    d.fresh_box()
    d.draw_text(5,   5,  gm_dt, d.date_font, d.white, d.drk_grn)
    show_logo()
    d.draw_text(40, 75,  f"No {team_name}" , d.score_font, d.white, d.drk_grn)
    d.draw_text(40, 125, f"Game Today!"    , d.score_font, d.white, d.drk_grn)
    
    
while True:
    
    DEBUG=True
    
    import gc
    gc.collect()
    
    global games
    factory_test = False
    force_offseason = False
    
    print(f"Version: {version}")
    yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
    short_yr = f"{int( str(yr)[2:]):02d}"
    gm_dt = f"{mt}/{dy}/{yr}"
    news_file = f"news.{mt}-{dy}-{yr}.txt"
    
    print("Date: ",gm_dt)
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    print("Month is",mt)
        
    try:
        if force_offseason:
            off_season()
        elif factory_test:
            run_factory_test()
        else:
            check_season()        
    except OSError as e:
        #Catch this known weird, unrecoverable issue and reboot
        #https://github.com/espressif/esp-idf/issues/2907
        if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
            import machine
            machine.reset()            

