import sys
import time
import re
import mrequests
    
""" SCREEN SETUP """
from hardware.screen_runner import display as d

""" All non caught errors are handled by main.py """  
from . team_id import team_id
start=5 
delta=45

""" BB SETUP """
from . import my_mlb_api
from hardware.ntp_setup import utc_to_local
url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
news_file = "news.txt"

""" Version """
from .version import version
   
def get_start_date(url, ua):
    global start_date
    import re
    import mrequests
    t=mrequests.get(url, headers={"User-Agent" : ua})
    _mtch= re.search("scheduled to begin on\s+([A-Z][a-z]+\s+[0-9]+)",t.text)
    if _mtch:
        try:
            start_date = _mtch.group(1)
        except IndexError as e:
            start_date = "??"
        finally:
            print(start_date)
            return start_date

def say_fetching(text='Fetching Data'):
    fresh_box()
    d.draw_text(5, 5, text, d.date_font, d.white, d.drk_grn)

def reg_season():
    global games
    games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
    
def off_season():
    days_til_open()
    gc.collect()
    show_filler_news(off_season)
    gc.collect()
    time.sleep(60 * 60 * 24 ) # check back Tommorow

def days_til_open():
    get_open_day()
    show_open_day()
   
def get_open_day():
    say_fetching()
    get_start_date(url, ua)

def show_open_day():
    fresh_box()
    d.draw_text(5,    start + (0 * delta)      ,f"{mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
    d.draw_text(42,   start + (1 * delta) + 25 ,f"Opening Day"         , d.score_font, d.white , d.drk_grn)
    d.draw_text(127,  start + (2 * delta) + 25 ,f"is"                  , d.score_font, d.white , d.drk_grn)
    d.draw_text(65,   start + (3 * delta) + 25 ,f"{start_date}"        , d.score_font, d.white , d.drk_grn)
    
def get_latest_news():
    url="https://www.mlb.com/news/"
    r = mrequests.get(url,headers={b"accept": b"text/html"})
    if r.status_code == 200:
        r.save(news_file)
        print("News saved to '{}'.".format(news_file))
    else:
        print("Request failed. Status: {}".format(r.status_code))
    r.close()

def get_news_from_file():
    global news
    news=[]
    with open(news_file) as fh:
        for line in fh:
            story = re.search('data-headline="(.*?)"',line)
            if story is not None:
                news.append(story.group(1))
    return news
                
def clear_story_area():
    d.fill_rectangle(1, 55, 318, 140, d.drk_grn)
    
def cycle_stories(func):
    count=0 ; ssleep =7
    while count < 475:     #On Average ~ 23.5 hours
        for story in news:
            print(f"=={count}")
            if count % 7 == 0:
                func()
                time.sleep(ssleep)
                clear_story_area()
            else:
                d.draw_text(5, start + (0 * delta), f"MLB News: {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
                """ Díaz - í is not supported by the font, make it a simple 'i' """
                story = story.replace('\xed','i')
                d.draw_text(35, 200, "Story at mlb.com", d.date_font,  d.white , d.drk_grn)
                d.scroll_print(text=story, y_pos=70, x_pos=8,
                               scr_len=18, clear=False, font=d.date_font,
                               bg=d.drk_grn, fg=d.white)
                """ x_pos for fill_rectangle must be at 1     """
                """ to keep vert lines from being overwritten """
                time.sleep(ssleep)
                clear_story_area()
            count+=1

def show_filler_news(func):
    get_latest_news()
    say_fetching("Fetching News")
    news=get_news_from_file()
    fresh_box()
    cycle_stories(func)

def fresh_box():
    d.clear_fill()
    d.draw_outline_box()

def run_factory_test():
    #If no game that day games will be empty, not undefined
    global games
    games = []
    check_if_game()
    from .test_games import games
    for x in games:
        games = [x]
        check_if_game()

def get_x_p(pname):
    """ Given 'John Smith (Jr.)'  """
    """ return 'J.Smith'          """
    fn,ln, *_ = pname.split(' ')
    fi = list(fn.split(' ')[0])[0]
    pn = fi + '.' + ln
    return pn        

def show_no_gm():
    yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
    fresh_box()
    d.draw_text(5, 5, gm_dt, d.date_font, d.white, d.drk_grn)
    d.draw_text(5, 75, 'No Game Today!', d.date_font, d.white, d.drk_grn)
    print(f"No Game today!")
    
def no_gm():
    show_no_gm()
    time.sleep(60)
    show_filler_news(show_no_gm)    

def check_if_game():
    if not games:
        no_gm()
        time.sleep(60 * 60 * 4)  # check back 4 hours from now
    else:
        print(games[0])
        what_sleep=get_score()
        print(f"Sleeping {what_sleep} seconds")
        time.sleep(what_sleep)         

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
            
            if factory_test == "True":
                return 5
            return 60 * 1# check back every x minutes
        
        elif game_status == "Game Over" or game_status == "Final":
            
            """ Stretch the Game Status to minimize ghost pixelation """
            """ here and with ZZZ in Warm up  below                  """
            
            game_status = "Final Score"
            lp = get_x_p(games[0]['losing_pitcher'])
            wp = get_x_p(games[0]['winning_pitcher'])
            
            d.clear_fill()
            d.draw_text(5, start + (0 * delta), f"{mt}-{dy}-{short_yr} {game_status}" , d.date_font,  d.white , d.drk_grn)
            d.draw_text(5, start + (1 * delta), f"{team1}:{team1_score} H {home_rec}" , d.score_font, d.white , d.drk_grn)
            d.draw_text(5, start + (2 * delta), f"{team2}:{team2_score} A {away_rec}" , d.score_font, d.white , d.drk_grn)
            d.draw_text(5, start + (3 * delta), f"WP: {wp}"                           , d.sm_font,    d.white , d.drk_grn)
            d.draw_text(5, start + (4 * delta), f"LP: {lp}"                           , d.sm_font,    d.white , d.drk_grn)
            d.draw_outline_box()
            
            if factory_test == "True":
                return 5
            return 60 * 60 *4 # check back 4 hours from now
        
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
            
            if factory_test == "True":
                return 5
            return 60 * 20 # check back every 20 minutes
        

while True:
    
    global games
    import gc
    gc.collect()
    factory_test = True
    force_offseason = False
    print(f"Version: {version}")
    yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
    short_yr = f"{int( str(yr)[2:]):02d}"
    gm_dt = f"{mt}/{dy}/{yr}"
    print("Date: ",gm_dt)
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    print("Month is",mt)
    
    if factory_test:
        run_factory_test()
    else:
        pass
    
    if force_offseason:
        off_season()
    else:
        pass
    
    if int(mt) in [11,12,01,02,03]:

        if int(mt) == 3 and int(dy) == 30:
            reg_season()
        off_season()
        
    else:
        
        try:
            reg_season()
        except OSError as e:
            #Catch this known weird, unrecoverable issue and reboot
            #https://github.com/espressif/esp-idf/issues/2907
            if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
                import machine
                machine.reset()
        else:
            check_if_game()           
