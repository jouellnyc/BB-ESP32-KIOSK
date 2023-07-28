""" All non caught errors are handled by main.py """  

""" SCREEN SETUP """ 
from hardware.screen_runner import display as d

""" Python Imports """
import utime
import time
import urequests
import ujson

""" App Imports / Globals """
from bbapp.team_id import team_id, team_name, team_code
from bbapp.team_colors import TEAM_COLORS
from hardware.ili9341 import color565
from .time_funcs import utc_to_local, tz_name

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
        self.start= 5 
        self.delta= 45
        self.previous_play  = None
        self.runners_not_changed = False
        self.play_not_changed_or_no_play = False
        self.bases = {'1st':None, '2nd': None, '3rd':None }
        
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

            
    def check_season(self):
        if (int(mt) in [04, 05, 06, 07, 08, 09, 10]) or \
           (int(mt) == 3 and (int(dy) == 30 or int(dy) == 31)):
            print("It's the Regular Season") 
            self.reg_season()
        else:
            print("Off Season")
            self.off_season()

    def reg_season(self):
        self.get_todays_games()
        self.check_if_game()
        
    def get_todays_games(self):
        if test_regular_season is True:
            self.regular_season_test()
        else:
            print("\n")                                      if DEBUG else None
            print("##### Connecting to MLB live sched data") if DEBUG else None
            self.games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
            if self.games:
                self.game_id=self.games[0].get('game_id','NA')
                print("Games", self.games) if DEBUG else None
            if len(self.games) > 1:
                print("More that one game Today!")
                if self.games[0]['status'] == "Final":
                    self.games[0]=self.games[1]        
            

    def check_if_game(self):
        if not self.games:
            self.no_gm()
        else:
            self.show_gm(sleep=7)
        
    def show_gm(self, sleep=7):
        print(f"> Game: {self.games[0]}")
        print(f"Status: {self.games[0]['status']}")
        self.set_teams()
        self.set_game_data_from_initial()
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
            print('Who: We are the home team - set teams') if DEBUG else None
        else:
            print('Who: We are the away team - set teams') if DEBUG else None
            
    def set_team_colors(self):
        self.home_team = str([x["teamCode"] for x in __all_team_ids["teams"] if x["id"] == self.home_id][0]).upper()
        self.away_team = str([x["teamCode"] for x in __all_team_ids["teams"] if x["id"] == self.away_id][0]).upper()
        _r, _g, _b = TEAM_COLORS[self.home_team]
        self.home_team_color = color565(_r, _g, _b)
        _r, _g, _b = TEAM_COLORS[self.away_team]
        self.away_team_color = color565(_r, _g, _b)
        
    def set_game_data_from_initial(self):
        if team_id == self.home_id:
            print('We are the home team - init')
        self.game_status = self.games[0]['status']
        self.home_score  = self.games[0].get("home_score",'NA')
        self.away_score  = self.games[0].get("away_score",'NA')
        self.home_rec    = self.games[0].get('home_rec','NA')
        self.away_rec    = self.games[0].get('away_rec','NA')
        if self.game_status == "Game Over" or self.game_status == "Final":
            self.lp          = self.games[0]['losing_pitcher']
            self.wp          = self.games[0]['winning_pitcher']
            
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
                print(f"Sleeping for {func_sleep} in cycle stories for {func.__name__}") 
                time.sleep(func_sleep)
                self.clear_story_area()
            else:
                d.draw_text(5, self.start + (0 * self.delta), f"MLB News: {mt}-{dy}-{short_yr}" , d.date_font,  d.white , d.drk_grn)
                """ Díaz - í is not supported by the font, make it a simple 'i' """
                story = self.rm_accents(story)
                d.draw_text(42, 215, "Story at mlb.com", d.sm_font,  d.white , d.drk_grn)
                d.scroll_print(text=story, y_pos=60, x_pos=18,
                               scr_len=18, clear=False, font=d.date_font,
                               bg=d.drk_grn, max_x=232, fg=d.white, debug=True) 
                """ x_pos for fill_rectangle must be at 1     """
                """ to keep vert lines from being overwritten """
                print(f"Sleeping for {story_sleep} in cycle stories_else {__name__}") if DEBUG else None
                time.sleep(story_sleep)
                self.clear_story_area()
            story_count+=1
    
    def get_x_p(self, pname):
        """ Given 'John Smith (Jr.)'  """
        """ return 'J.Smith'          """
        print("pname", pname) if DEBUG else None
        fn, *ln = pname.split(' ')
        fi = fn[0]
        ln = ' '.join(ln)
        pn = fi + '.' + ln
        return pn
    
    def get_current_game_data(self):
        url=f"https://statsapi.mlb.com/api/v1.1/game/{self.game_id}/feed/live?fields=gamePk,liveData,plays,currentPlay,result,description,awayScore,homeScore,about,batter,count,inning,halfInning,balls,strikes,outs,matchup,postOnFirst,postOnSecond,postOnThird,fullName,gameData,status,detailedState,decisions,winner,loser"
        print(f"##### Connecting to MLB live play data") if DEBUG else None
        self.current_game_data = ujson.loads(urequests.get(url, headers=http_headers).text)
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
            "Postponed"
            "Manager challenge: XXX"
        """
        self.game_status = self.current_game_data['gameData']['status']['detailedState']
        if 'hallenge' in self.game_status:
            self.game_status = 'Manager challenge'
        if 'eview' in self.game_status:
            self.game_status = 'Umpire Review'
        print("GS: ", self.game_status) if DEBUG else None
        
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
        
    def show_current_game(self):

        while any([x in self.game_status for x in ["eview", "hallenge", "In Progress"]]):

            def exec_game_details():
                self.get_current_game_data()
                d.gc_status_flush(MEM_DEBUG=False)
                self.set_game_status()
                self.set_current_play()
                self.set_scores()
        
            exec_game_details()
            print('self.game_status', self.game_status) if DEBUG else None
            
            self.balls    = self.currentPlay['count']['balls']
            self.strks    = self.currentPlay['count']['strikes']
            self.outs     = self.currentPlay['count']['outs']
            self.inn_cur  = self.currentPlay['about']['inning']
            self.in_sta   = self.currentPlay['about']['halfInning']
            self.in_sta   = self.in_sta[0].upper() + self.in_sta[1:]
            self.batter   = self.get_x_p(self.currentPlay['matchup']['batter']['fullName'])
            
            self.clear_leave_outline()
            
            if "Bottom" in self.in_sta:
                self.up=f"{self.home_team} up"
            elif "Top" in self.in_sta:
                self.up=f"{self.away_team} up"
            elif "End" or "Middle" in self.in_sta:
                self.up=f"{mt}-{dy}-{short_yr}"
            
            """ Show the Current Score """
            if any(x in self.game_status for x in ["hallenge", "eview"]):
                self.show_in_progress(Time_Out_Status=True)
            else:
                self.show_in_progress()
            in_progress_sleep=5
            if self.play_not_changed_or_no_play: 
                in_progress_sleep+=1
            if self.runners_not_changed:
                in_progress_sleep+=1
                
            print(f"#### sleeping {in_progress_sleep} after showing score/in_progress")
            time.sleep(in_progress_sleep)
            d.gc_status_flush(MEM_DEBUG=False)
            
            self.cur_play_res  = self.currentPlay.get('result', {}).get('description')

            """ Check the Current play vs Previous Play """
            """ current_play_index may or may not have 'result' => 'description' """
            """ allPlays'][current_play_index] may have it's 'result' => 'description' updated from the 'current' to the final one """

            print(f"Plays -  self.cur_play_res: {self.cur_play_res} previous_play: {self.previous_play}") if DEBUG else None
            
            if self.cur_play_res is not None:
                
                if self.cur_play_res != self.previous_play:
                    print(f"#### Play change: {self.cur_play_res}")
                    self.previous_play = self.cur_play_res
                    self.clear_story_area()
                    d.draw_text(5, self.start + (0 * self.delta), f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}", d.date_font,  d.white , d.drk_grn)
                    if len(self.cur_play_res.split(' ')) > 12:
                        sp_font=d.sm_font; sp_max_x=300; sp_scr_len=26
                        play_check_sleep=7
                    else:
                        sp_font=d.date_font; sp_max_x=230; sp_scr_len=18
                        play_check_sleep=4
                    d.scroll_print(text=self.cur_play_res, y_pos=60, x_pos=18, scr_len=sp_scr_len, max_x=sp_max_x,
                                   clear=False, font=sp_font, bg=d.drk_grn, fg=d.white)
                    print(f"# Sleeping {play_check_sleep} after Current Play change")
                    time.sleep(play_check_sleep)
                    
                else:
                    print(f"# Play change: No")
                    self.play_not_changed_or_no_play = True
            else:
                self.play_not_changed_or_no_play = True
                print("# Play is None")
            
            d.gc_status_flush(MEM_DEBUG=False)
            
            """ Now, Check Runners """
            runners = self.current_game_data['liveData']['plays']['currentPlay']['matchup']
            if self.runners_changed(runners):
                print('#### Runners Changed')
                self.show_runners(front=False)
                runners_sleep=4
                print(f"Sleeping {runners_sleep} after runners change")
                time.sleep(runners_sleep)
            else:
                print('Runners Did not Change')
                self.runners_not_changed = True
            d.gc_status_flush(MEM_DEBUG=False)
            
            #New line to separate the plays is easier on the eyes, just before "Connecting to MLB ..."
            print()
            
            if test_regular_season:
                print("Testing Regular Season")
                return 2
            
        else:
            
            if self.game_status == "Game Over" or self.game_status == "Final":
                
                self.get_todays_games()
                self.set_game_data_from_initial()
                
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
                self.show_filler_news(self.show_scheduled, func_sleep=fsleep)
                return 1
            
            
            elif self.game_status == "Warmup":
                self.show_scheduled()
                if test_regular_season:
                    return 2
                return 60 * 2# check back every 2 minutes
            
            
            else:  #"Pre Game / Delayed / Postponed"
                self.show_scheduled()
                if test_regular_season:
                    return 2
                return 60 * 10 # check back every 10 minutes

    def show_in_progress(self, Time_Out_Status=False):
        print(f"balls:{self.balls} strikes:{self.strks} outs:{self.outs}")  if DEBUG else None
        print(f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}")           if DEBUG else None
        if Time_Out_Status:
            d.draw_text(5, self.start + (0 * self.delta),     f"{self.game_status}", d.date_font,  d.white , d.drk_grn)
        else:
            d.draw_text(5, self.start + (0 * self.delta),     f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}", d.date_font,  d.white , d.drk_grn)
        d.draw_text(5, self.start + (1 * self.delta) + 5, f"{self.home_team}:{self.away_score} H {self.home_rec}" , d.score_font, d.white , self.home_team_color)
        d.draw_text(5, self.start + (2 * self.delta) + 5, f"{self.away_team}:{self.home_score} A {self.away_rec}" , d.score_font, d.white , self.away_team_color)
        d.draw_text(5, self.start + (3 * self.delta) + 5, f"AB: {self.batter}"                                    , d.sm_font,    d.white , d.drk_grn)
        d.draw_text(10,self.start + (4 * self.delta) + 5, f"B: {self.balls} S: {self.strks} O: {self.outs }"      , d.sm_font,    d.white , d.drk_grn)
        self.show_runners(front=True)
        d.draw_outline_box()
            
    def no_gm(self, sleep=7):
        self.show_no_gm()
        print(f"Sleeping for {sleep} seconds in show_no_gm")
        time.sleep(sleep)
        self.show_filler_news(self.show_no_gm)    

    def off_season(self, sleep=30):
        print("start off season") if DEBUG else None
        self.opening_day_screen()
        print(f"Sleeping for {sleep} seconds in off_season")
        time.sleep(sleep)
        gc.collect()
        show_filler_news(opening_day_screen)
        gc.collect()

    def opening_day_screen(self):
        print("start opening_day_screen") if DEBUG else None
        d.fresh_box()
        self.show_logo()
        d.draw_text(5,    self.start + (0 * self.delta)      ,f"{mt}-{dy}-{short_yr}", d.date_font,  d.white , d.drk_grn)
        d.draw_text(42,   self.start + (1 * self.delta) + 25 ,f"Opening Day"         , d.score_font, d.white , d.drk_grn)
        d.draw_text(127,  self.start + (2 * self.delta) + 25 ,f"is"                  , d.score_font, d.white , d.drk_grn)
        d.draw_text(65,   self.start + (3 * self.delta) + 25 ,f"{opening_day}"       , d.score_font, d.white , d.drk_grn)


    def regular_season_test(self):
        #If no game that day games will be empty, not undefined
        from .test_games import games
        print(f"Games {games}")
        for x in games:
            self.games = [x]
            self.check_if_game()
        self.games = []
        self.check_if_game()

    def rm_accents(self, story):
        """ Replace Accent Accent aigu, grave, and unicode apostrophes """
        
        """ First Pass thanks to ChatGPT """
        replacements = {
            "à": "a",
            "â": "a",
            "ç": "c",
            "é": "e",
            "è": "e",
            "ê": "e",
            "ë": "e",
            "î": "i",
            "ï": "i",
            "ô": "o",
            "ù": "u",
            "û": "u",
            "ü": "u",
            "À": "A",
            "Â": "A",
            "Ç": "C",
            "É": "E",
            "È": "E",
            "Ê": "E",
            "Ë": "E",
            "Î": "I",
            "Ï": "I",
            "Ô": "O",
            "Ù": "U",
            "Û": "U",
            "Ü": "U",
        }

        for accented, non_accented in replacements.items():
            story = story.replace(accented, non_accented)
    
        """ Second Pass thanks to Empirical Evidence """
        return story.replace('\xed','i').replace('\xe9','e').replace('\xc0','A')\
                    .replace('\xe8','e').replace('\xec','i').replace('\xd2','O')\
                    .replace('\xf9','u').replace('\xc9','E').replace('\xe1','a')\
                    .replace('\xcd','I').replace('\xf3','o').replace('\xda','U')\
                    .replace(u"\u2018", "'").replace(u"\u2019", "'")\
                    .replace(u'\xa0', u' ').replace(u'\xc1','A').replace('\xf1','n')

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
        d.fresh_box()
        self.cycle_stories(func, news, func_sleep=30)

    def show_final(self):
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
        self.set_team_color()
        self.show_logo()
        d.draw_text(40, 75,  f"No {team_name}" , d.score_font, d.white, self.your_team_color)
        d.draw_text(40, 125, f"Game Today!"    , d.score_font, d.white, self.your_team_color)

    
    def onbase(self, ax, bx, cx, dx):
        d.fill_polygon(ax, bx, cx, dx, d.white, rotate=0)

    def empty(self, ax, bx, cx, dx):
        d.draw_polygon(ax, bx, cx, dx, d.white, rotate=0)
            
    def show_runners(self, front=False):
        
        if front:
            
            print('Show Runners bases Front',self.bases)
            diamonds = { '1st' : [4, 275, 200,10],
                         '2nd' : [4, 250, 165,10] ,
                         '3rd' : [4, 225, 200,10] }
        else:
    
            print('Show Runners bases Large',self.bases)
            diamonds = { '1st' : [4, 215, 150,15],
                         '2nd' : [4, 155, 75, 15] ,
                         '3rd' : [4, 95, 150, 15] }
            
            text = {  '1st' : [195, 180 ],
                       '2nd' : [95, 100 ],
                       '3rd' : [2, 180] }
        
            d.fresh_box()
            d.draw_text(5, self.start + (0 * self.delta),
                        f"{self.in_sta} {self.inn_cur}{ordinals[self.inn_cur]} {self.up}",
                        d.date_font,  d.white , d.drk_grn)
        
        for one_base in diamonds.keys():

            if self.bases[one_base]:
                
                self.onbase(ax=diamonds[one_base][0], bx=diamonds[one_base][1],
                            cx=diamonds[one_base][2], dx=diamonds[one_base][3])
                
                if front is False:
                    d.draw_text(text[one_base][0], text[one_base][1],
                                self.get_x_p(self.bases[one_base]), d.sm_font, d.white , d.drk_grn)
                
            else:
                self.empty(ax=diamonds[one_base][0], bx=diamonds[one_base][1],
                           cx=diamonds[one_base][2], dx=diamonds[one_base][3])
        

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

bb=BBKiosk()
bb.set_team_color()
n = News()

while True:

    from .time_funcs import dy, mt, short_yr, game_day_now
    gm_dt = game_day_now()
    
    params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
    
    import gc
    gc.collect()
    print(f"==== Version: {version}")
    
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
    except ValueError as e:
        if 'BadStatusLine' in str(e):
            d.fresh_box(); secs=60
            msg=f"HTTP bad status line: sleeping for {secs} seconds"
            d.scroll_print(msg, y_pos=80, x_pos=18, scr_len=18,
                           clear=False, font=d.date_font, bg=d.drk_grn,
                           max_x=232, fg=d.white, debug=True)
            time.sleep(secs)