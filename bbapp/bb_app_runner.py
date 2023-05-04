""" All non caught errors are handled by main.py """  

""" SCREEN SETUP """ 
from hardware.screen_runner import display as d

""" Python Imports """
import os
import sys
import utime
import time
import urequests
import ujson

""" App Imports / Globals """
from bbapp.team_id import team_id, team_name, team_code
from bbapp.team_colors import TEAM_COLORS
from hardware.ili9341 import color565
from hardware.ntp_setup import utc_to_local, timezone, tz_name
from . import my_mlb_api
from .news import News
from .version import version

""" There is no need to exec this multiple times """
def get_all_team_ids():
        with open("/bbapp/team_ids.py") as f:
            return ujson.loads(f.read())

__all_team_ids = get_all_team_ids()


class BBKiosk:

    def __init__(self):
        self.bases = {'1st':None, '2nd': None, '3rd':None }
        self.previous_play  = None
        self.start= 5 
        self.delta= 45

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

            
    #@timing_decorator        
    def check_season(self):
        if (int(mt) in [04, 05, 06, 07, 08, 09, 10]) or \
           (int(mt) == 3 and (int(dy) == 30 or int(dy) == 31)):
            print("It's the Regular Season") 
            self.reg_season()
        else:
            print("Off Season")
            self.off_season()

    #@timing_decorator
    def reg_season(self):
        self.check_if_game()
        
    def check_if_game(self):
        self.get_todays_games()
        if not self.games:
            self.no_gm()
        else:
            self.show_gm(sleep=7)

    #@timing_decorator
    def get_todays_games(self):
        print("Connecting to MLB live sched data") if DEBUG else None
        self.games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
        if len(self.games) > 1:
            print("More that one game Today!")
            if self.games[0]['status'] == "Final":
                self.games[0]=self.games[1]
        self.game_id=self.games[0].get('game_id','NA')

    def show_gm(self, sleep=7):
        print(f"> Game: {self.games[0]}")
        print(f"Status: {self.games[0]['status']}")
        self.set_teams()
        what_sleep=self.show_current_game()
        print(f" Sleeping {what_sleep} seconds after get_score") if DEBUG else None
        time.sleep(what_sleep)

    def set_teams(self):
        self.set_team_records()
        self.set_team_ids()
        self.set_team_colors()

    def set_team_records(self):
        """ Records """
        self.home_rec = self.games[0].get('home_rec','NA')
        self.away_rec = self.games[0].get('away_rec','NA')
        
    def set_team_ids(self):
        """ Determine home or away from Team Ids Data """
        self.home_id = self.games[0].get("home_id",'NA')
        self.away_id = self.games[0].get("away_id",'NA')
        """ These are both strings - Reminder """
        if team_id == self.home_id:
            print('Who: We are the home team')
        else:
            print('We are the away team')
        
    def set_team_colors(self):
        self.home_team = str([x["teamCode"] for x in __all_team_ids["teams"] if x["id"] == self.home_id][0]).upper()
        self.away_team = str([x["teamCode"] for x in __all_team_ids["teams"] if x["id"] == self.away_id][0]).upper()
        _r, _g, _b = TEAM_COLORS[self.home_team]
        self.home_team_color = color565(_r, _g, _b)
        _r, _g, _b = TEAM_COLORS[self.away_team]
        self.away_team_color = color565(_r, _g, _b)
        
    def clear_story_area(self):
        d.fill_rectangle(1, 41, 318, 198, d.drk_grn)

    def clear_status_area(self):
        d.fill_rectangle(1, 1, 318, 38, d.drk_grn)
        
    def clear_leave_outline(self):
        self.clear_status_area()
        self.clear_story_area()
        
    def cycle_stories(self, func, news=0, func_sleep=30):
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
                self.clear_story_area()
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
                self.clear_story_area()
            story_count+=1

    def gc_status_flush(self):
        print("Mem: ", gc.mem_free()) if MEM_DEBUG else None
        gc.collect()
        print("Mem: ", gc.mem_free()) if MEM_DEBUG else None
    
    def get_x_p(self, pname):
        """ Given 'John Smith (Jr.)'  """
        """ return 'J.Smith'          """
        print("pname", pname) if DEBUG else None
        fn,ln, *_ = pname.split(' ')
        fi = list(fn.split(' ')[0])[0]
        pn = fi + '.' + ln
        return pn        
    
    #@timing_decorator
    def get_current_game_data(self):
        url=f"https://statsapi.mlb.com/api/v1.1/game/{self.game_id}/feed/live?fields=gamePk,liveData,plays,currentPlay,result,description,awayScore,homeScore,about,batter,count,inning,halfInning,balls,strikes,outs,matchup,postOnFirst,postOnSecond,postOnThird,fullName,gameData,status,detailedState,decisions,winner,loser"
        print(f"Connecting to MLB live data at {url}") if DEBUG else None
        self.current_game_data = ujson.loads(urequests.get(url).text)
        print('current_game_data', self.current_game_data) if DEBUG else None
       
                                                   
    def set_game_status(self):
        """ Status Check - Statuses are one of:
            "In Progress"
            "Umpire Review"?
            "Scheduled"
            "Pre-Game"
            "Warmup"
            "Final"
            "Game Over"
            "Delayed"
            "Manager challenge: XXX"""
        self.game_status = self.current_game_data['gameData']['status']['detailedState']
        
    def set_current_play(self):
        try:
            self.currentPlay = self.current_game_data['liveData']['plays']['currentPlay']
        except KeyError:
            print(f"No currentPlay")
        else:
            print(f"The currentPlay: {self.currentPlay}")
    
    def set_scores(self):
        self.away_score  = self.currentPlay['result']['awayScore']
        self.home_score  = self.currentPlay['result']['homeScore']
        
    #@timing_decorator
    def show_current_game(self):

        def exec_game_details():
            self.get_current_game_data()
            self.gc_status_flush()
            self.set_game_status()
            self.set_current_play()
            self.set_scores()
        
        """ All of the statuses need at least some of these methods """
        exec_game_details()
        
        while (self.game_status == "In Progress")  or (( "eview" or "challenge" ) in self.game_status):

            self.balls    = self.currentPlay['count']['balls']
            self.strks    = self.currentPlay['count']['strikes']
            self.outs     = self.currentPlay['count']['outs']
            self.inn_cur  = self.currentPlay['about']['inning']
            self.in_sta   = self.currentPlay['about']['halfInning']
            self.in_sta   = self.in_sta[0].upper() + self.in_sta[1:]
            self.batter   = self.get_x_p(self.currentPlay['matchup']['batter']['fullName'])
            
            #d.clear_fill()
            self.clear_leave_outline()
            
            if "Bottom" in self.in_sta:
                self.up=f"{self.home_team} up"
            elif "Top" in self.in_sta:
                self.up=f"{self.away_team} up"
            elif "End" or "Middle" in self.in_sta:
                self.up=f"{mt}-{dy}-{short_yr}"
            
            """ Show the Current Score """
            self.show_in_progress()
            in_progress_sleep=5
            print(f"sleeping {in_progress_sleep} after showing score/in_progress")
            time.sleep(in_progress_sleep)
            self.gc_status_flush()
            
            self.cur_play_res  = self.currentPlay.get('result', {}).get('description')

            """ Check the Current play vs Previous Play """
            """ current_play_index may or may not have 'result' => 'description' """
            """ allPlays'][current_play_index] may have it's 'result' => 'description' updated from the 'current' to the final one """

            print(f"Plays -  self.cur_play_res: {self.cur_play_res} previous_play: {self.previous_play}") if DEBUG else None
            
            if self.cur_play_res is not None:
                
                if self.cur_play_res != self.previous_play:
                    print(f"Play change: {self.cur_play_res}")
                    self.previous_play = self.cur_play_res
                    ####d.fresh_box()
                    self.clear_story_area()
                    #d.draw_text(5,  start + (0 * delta), f"{in_sta} {inn_cur}{ordinals[inn_cur]} {mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
                    d.draw_text(5, self.start + (0 * self.delta), f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}", d.date_font,  d.white , d.drk_grn)
                    if len(self.cur_play_res.split(' ')) > 12:
                        sp_font=d.sm_font; sp_max_x=300; sp_scr_len=26
                    else:
                        sp_font=d.date_font; sp_max_x=230; sp_scr_len=18
                    d.scroll_print(text=self.cur_play_res, y_pos=60, x_pos=18, scr_len=sp_scr_len, max_x=sp_max_x,
                                   clear=False, font=sp_font, bg=d.drk_grn, fg=d.white)
                    
                else:
                    print(f"Play change: No")
            else:
                print("Play is None")
                
            play_check_sleep=4
            print(f"Sleeping {play_check_sleep} after Current Play Check/Show")
            time.sleep(play_check_sleep)
            self.gc_status_flush()
                        
            
            """ Now, Check Runners """
            runners = self.current_game_data['liveData']['plays']['currentPlay']['matchup']
            if self.runners_changed(runners):
                print('Runners Changed')
                self.show_runners(runners)
            else:
                print('Runners Did not Change')
            runners_sleep=4
            print(f"Sleeping {runners_sleep} after runners")
            time.sleep(runners_sleep)
            self.gc_status_flush()
            
            if test_regular_season:
                print("Testing Regular Season")
                return 2
            
            exec_game_details()
            
        else:
            
        
            if self.game_status == "Game Over" or self.game_status == "Final":
                
                """ Stretch the Game Status to minimize ghost pixelation """
                """ here and with ZZZ in Warm up  below                  """
                if test_regular_season:
                    fsleep=5
                else:
                    fsleep=30            
                self.show_final()
                print(f'sleeping for {fsleep} in  {self.game_status}') if DEBUG else None
                time.sleep(fsleep)
                self.show_filler_news(self.show_final, func_sleep=fsleep)
                return 1
            
            elif self.game_status == "Scheduled":
                if test_regular_season:
                    fsleep=5
                else:
                    fsleep=30            
                self.show_scheduled()
                print(f'sleeping for {fsleep} in  {self.game_status}') if DEBUG else None
                time.sleep(fsleep)
                self.show_filler_news(show_scheduled, func_sleep=fsleep)
                return 1
            
            
            elif self.game_status == "Warmup":
                self.show_scheduled()
                if test_regular_season:
                    return 2
                return 60 * 2# check back every 2 minutes
            
            
            else:  #"Pre Game / Delayed"
                self.show_scheduled()
                if test_regular_season:
                    return 2
                return 60 * 10 # check back every 10 minutes

    def show_in_progress(self):
        print(f"balls:{self.balls} strikes:{self.strks} outs:{self.outs}")  if DEBUG else None
        print(f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}")           if DEBUG else None
        d.draw_text(5, self.start + (0 * self.delta),     f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}", d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, self.start + (1 * self.delta) + 5, f"{self.home_team}:{self.away_score} H {self.home_rec}" , d.score_font, d.white , self.home_team_color)
        d.draw_text(5, self.start + (2 * self.delta) + 5, f"{self.away_team}:{self.home_score} A {self.away_rec}" , d.score_font, d.white , self.away_team_color)
        d.draw_text(5, self.start + (3 * self.delta) + 5, f"AB: {self.batter}"                                    , d.sm_font,    d.white , d.drk_grn)
        d.draw_text(10,self.start + (4 * self.delta) + 5, f"B: {self.balls} S: {self.strks} O: {self.outs }"      , d.sm_font,    d.white , d.drk_grn)
        self.show_runners_front()
        d.draw_outline_box()
            
    def no_gm(sleep=7):
        self.show_no_gm()
        print(f"Sleeping for {sleep} seconds in show_no_gm")
        time.sleep(sleep)
        self.show_filler_news(show_no_gm)    

    def off_season(sleep=30):
        print("start off season") if DEBUG else None
        self.opening_day_screen()
        print(f"Sleeping for {sleep} seconds in off_season")
        time.sleep(sleep)
        gc.collect()
        show_filler_news(opening_day_screen)
        gc.collect()

    def opening_day_screen():
        print("start opening_day_screen") if DEBUG else None
        d.fresh_box()
        self.show_logo()
        d.draw_text(5,    self.start + (0 * self.delta)      ,f"{mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
        d.draw_text(42,   self.start + (1 * self.delta) + 25 ,f"Opening Day"         , d.score_font, d.white , d.drk_grn)
        d.draw_text(127,  self.start + (2 * self.delta) + 25 ,f"is"                  , d.score_font, d.white , d.drk_grn)
        d.draw_text(65,   self.start + (3 * self.delta) + 25 ,f"{opening_day}"       , d.score_font, d.white , d.drk_grn)


    def regular_season_test():
        #If no game that day games will be empty, not undefined
        from .test_games import games
        print(f"Games {games}")
        for x in games:
            self.games = [x]
            check_if_game()
        self.games = []
        self.check_if_game()

    def rm_accents(story):
        """ Replace Accent Accent aigu, grave, and unicode apostrophes """
        return story.replace('\xed','i').replace('\xe9','e').replace('\xc0','A')\
                    .replace('\xe8','e').replace('\xec','i').replace('\xd2','O')\
                    .replace('\xf9','u').replace('\xc9','E').replace('\xe1','a')\
                    .replace('\xcd','I').replace('\xf3','o').replace('\xda','U')\
                    .replace(u"\u2018", "'").replace(u"\u2019", "'")\
                    .replace(u'\xa0', u' ').replace(u'\xc1','A')

    def runners_changed(self, runners):
        
        current_bases =  {}
        current_bases['1st']=runners.get('postOnFirst', {}).get('fullName')
        current_bases['2nd']=runners.get('postOnSecond', {}).get('fullName')
        current_bases['3rd']=runners.get('postOnThird' , {}).get('fullName')
        
        print('Inside Checking for runners changed : bases: ',  self.bases) if DEBUG else None
        print('Inside Checking for runners changed : current_bases:', current_bases) if DEBUG else None
        
        if current_bases != self.bases:
            self.bases = current_bases
            return True
        return False

    def say_fetching(self, text='Fetching Data'):
        d.fresh_box()
        d.draw_text(5, 5, text, d.date_font, d.white, d.drk_grn)
       
    def set_team_color(self):
        r, g, b = TEAM_COLORS[team_code.upper()]
        self.your_team_color = color565(r, g, b)

    def show_filler_news(self, func, func_sleep=30):
        print('In show_filler_news') if DEBUG else None
        self.say_fetching("Fetching News")
        news = n.get_latest_news()
        print(n.news) if DEBUG else None
        d.fresh_box()
        self.cycle_stories(func, news, func_sleep=30)

    def show_final(self):
        self.game_status = "Final Score"
        self.lp = self.get_x_p(self.current_game_data['liveData']['decisions']['winner']['fullName']) 
        self.wp = self.get_x_p(self.current_game_data['liveData']['decisions']['loser']['fullName'])
        d.clear_fill()
        d.draw_text(5, self.start + (0 * self.delta), f"{self.game_status} {mt}-{dy}-{short_yr}"              , d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, self.start + (1 * self.delta), f"{self.home_team}:{self.home_score} H {self.home_rec}" , d.score_font, d.white , self.home_team_color)
        d.draw_text(5, self.start + (2 * self.delta), f"{self.away_team}:{self.away_score} A {self.away_rec}" , d.score_font, d.white , self.away_team_color)
        d.draw_text(5, self.start + (3 * self.delta), f"WP: {self.wp}"                                        , d.sm_font,    d.white , self.home_team_color)
        d.draw_text(5, 0     + (4 * self.delta), f"LP: {self.lp}"                                             , d.sm_font,    d.white , self.away_team_color)
        d.draw_outline_box()

    def show_logo(self):
        print("start show_logo") if DEBUG else None
        d.draw_text(235, 5,  team_code.upper(), d.date_font, d.white, d.drk_grn)
        
    def show_no_gm(self):
        yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
        d.fresh_box()
        d.draw_text(5,   5,  gm_dt, d.date_font, d.white, d.drk_grn)
        self.show_logo()
        d.draw_text(40, 75,  f"No {team_name}" , d.score_font, d.white, your_team_color)
        d.draw_text(40, 125, f"Game Today!"    , d.score_font, d.white, your_team_color)

    def show_runners_front(self):

        def onbase():
            d.fill_polygon(ax, bx, cx, dx, d.white, rotate=0)

        def empty():
            d.draw_polygon(ax, bx, cx, dx, d.white, rotate=0)

        ax=4; bx=275; cx=200; dx=10
        if self.bases['1st']:
            onbase()
        else:
            empty()
            
        ax=4; bx=250; cx=165; dx=10
        if self.bases['2nd']:
            onbase()
        else:
            empty()
            
        ax=4; bx=225; cx=200; dx=10   
        if self.bases['3rd']:
            onbase()
        else:
            empty()


    def show_runners(self, runners):
        
        
        def onbase():
            d.fill_polygon(ax, bx, cx, dx, d.white, rotate=0)

        def empty():
            d.draw_polygon(ax, bx, cx, dx, d.white, rotate=0)

        d.clear_fill()
        d.draw_outline_box()
        #d.draw_text(5,  start + (0 * self.delta), f"{in_sta} {inn_cur}{ordinals[inn_cur]} {mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, self.start + (0 * self.delta),     f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}", d.date_font,  d.white , d.drk_grn)
        
        fn='fullName'
        what='postOnFirst'
        print('Show Runners bases ',self.bases)
        ax=4; bx=215; cx=150; dx=15
        if self.bases['1st']:
            d.draw_text(195, 180, self.get_x_p(self.bases['1st']), d.sm_font,    d.white , d.drk_grn) 
            onbase()
            
        else:
            empty()
        
        ax=4; bx=155; cx=75; dx=15
        if self.bases['2nd']:
            onbase()
            d.draw_text( 95, 100, self.get_x_p(self.bases['2nd']), d.sm_font,    d.white , d.drk_grn)
        else:
            empty()
        
        ax=4; bx=95; cx=150; dx=15
        if self.bases['3rd']:
            onbase()
            d.draw_text(  2, 180, self.get_x_p(self.bases['3rd']), d.sm_font,    d.white , d.drk_grn)
            
        else:
            empty()

    def show_scheduled(self):
        gm_time=self.games[0].get('game_datetime','NA')
        """ Take the UTC Time in MLB Api and display it in the local timezone """
        tm=utc_to_local(gm_time)
        d.clear_fill()
        d.draw_text(5, self.start + (0 * self.delta), f"{self.game_status} {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, self.start + (1 * self.delta), f"{self.home_team}:N H {self.home_rec}"    , d.score_font, d.white , self.home_team_color)
        d.draw_text(5, self.start + (2 * self.delta), f"{self.away_team}:N A {self.away_rec}"    , d.score_font, d.white , self.away_team_color)
        d.draw_text(5, self.start + (3 * self.delta), f"Game at {tm} {tz_name}"             , d.sm_font,    d.white , d.drk_grn)
        d.draw_text(5, self.start + (4 * self.delta), f"ZZZZZZZZZZZZZZZZZZZZZ"              , d.sm_font,   d.drk_grn, d.drk_grn)
        d.draw_outline_box()

""" Constants """
od_url='https://en.wikipedia.org/wiki/2023_Major_League_Baseball_season'
opening_day = 'March 30'
news_url="https://www.mlb.com/news/"
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
ordinals      = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th', 5: 'th', 6: 'th', 7: 'th', 8: 'th', 9: 'th', 10: 'th', 11: 'th', 12:'th'}
http_headers= { 'User-Agent': ua }

""" Debug Options """
force_offseason = False
test_regular_season = False
DEBUG = True
MEM_DEBUG = True


bb=BBKiosk()
bb.set_team_color()

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
            bb.off_season()
        elif test_regular_season:
            #Will go on infinitely ...
            bb.regular_season_test()
        else:
            bb.check_season()        
    except OSError as e:
        #Catch this known weird, unrecoverable issue and reboot
        #https://github.com/espressif/esp-idf/issues/2907
        if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
            import machine
            machine.reset()