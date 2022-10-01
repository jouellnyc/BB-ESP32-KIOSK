print('hellooo')

import time
time.sleep(5)

""" OLED SETUP """
from .esp32cam_oled import oled  as myoled
#from .pico_oled import oled  as myoled

print('hellooo1')

""" Wrap literally as much as possible to     """
""" display an error to the user in the field """

try:

    """ This is the only thing you need to lookup """
    """ see team_ids.py for your teams' id        """
    team_id = int(111)


    start=0
    delta=13

    import sys
    import time

    """ RGB SETUP """
    from . import rgb
    #from . import pico_rgb as rgb
    
    """ MLB SETUP """
    from . import my_mlb_api
    from .ntp_setup import utc_to_local

    """ Version """
    from .version import version

    def fill_show():
        myoled.fill(0)
        myoled.show()
        
    def get_x_p(pname):
        """ Given 'John Smith (Jr.)'  """
        """ return 'J.Smith'          """
        fn,ln, *_ = pname.split(' ')
        fi = list(fn.split(' ')[0])[0]
        pn = fi + '.' + ln
        return pn        

    def set_led_color():
        """ Are we happy or not ? """
        """ Green if winning, Red if not, Blue if tie """
        if our_score > opp_score:
           print("Setting Green")
           rgb.all_off()
           rgb.g.value(1)
        elif our_score < opp_score:
            print("Setting Red")
            rgb.all_off()
            rgb.r.value(1)
        elif our_score == opp_score:
            print("Setting Blue")
            rgb.all_off()
            rgb.b.value(1)

            
    def get_score():
            
            """ Team Ids """
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
                battr   = get_x_p(games[0].get("Batter",'NA'))
            
                fill_show()
                set_led_color()
                
                myoled.text(f"{mt}-{dy}-{short_yr}",                           0, start + (0 * delta))
                myoled.text(f"{hr}:{mn}"           ,                          72, start + (0 * delta))
                myoled.text(f"{team1}: {team1_score} (H)",                     0, start + (1 * delta) + 3)
                myoled.text(f"{team2}: {team2_score} (A)",                     0, start + (2 * delta))
                myoled.text(f"{in_sta} {inn_cur} B{balls} S{strks} O{outs}",   0, start + (3 * delta))
                myoled.text(f"ab: {battr}", 0, start + (4 * delta))
                myoled.show()
                return 60 * 1# check back every 2 minutes
            
            elif game_status == "Game Over" or game_status == "Final":
                
                lp = get_x_p(games[0]['losing_pitcher'])
                wp = get_x_p(games[0]['winning_pitcher'])
                
                fill_show()
                set_led_color()
                
                myoled.text(f"{mt}-{dy}-{short_yr} Final", 0, start + (0 * delta))
                myoled.text(f"{team1}:{team1_score} H {home_rec}", 0, start + (1 * delta) + 4)
                myoled.text(f"{team2}:{team2_score} A {away_rec}", 0, start + (2 * delta))
                myoled.text(f"wp: {wp}",                           0, start + (3 * delta))
                myoled.text(f"lp: {lp}",                           0, start + (4 * delta))
                myoled.show()
                return 60 * 60 *4 # check back 4 hours from now
            
            else:  #"Scheduled"/"Warm up"/"Pre Game"
                
                if 'Delayed' in  game_status:
                    print('setting led yellow')
                    rgb.g.value(1)
                    rgb.r.value(1)
                    rgb.b.value(0)
                else:
                    print('setting led white')
                    rgb.all_off() #Clear RGB LED and 
                    rgb.all_on()  #Set it  white
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
        yr, mt, dy, hr, mn, s1, s2, s3 = time.localtime()
        myoled.text(f"{mt}-{dy}-{short_yr}", 0, start + (0 * delta))
        myoled.text(f"No Game Today!", 0, start + (1 * delta) + 4)
        print(f"No Game today!")
        myoled.show()


    
    while True:
            
            count=0
            count+=1;print(count)
            import gc
            count+=1;print(count)
            gc.collect()
            count+=1;print(count)
            print(gc.mem_free())
            print(f"Version: {version}")
            count+=1;print(count)
            yr, mt, dy, hr, mn, s1, s2, s3 = [ f"{x:02d}" for x in time.localtime() ]
            short_yr = f"{int( str(yr)[2:]):02d}"
            gm_dt = f"{mt}/{dy}/{yr}"
            print("Date: ",gm_dt)
            
            params = {'teamId': team_id, 'startDate': gm_dt, 'endDate': gm_dt, 'sportId': '1', 'hydrate': 'decisions,linescore'}
            games = my_mlb_api.schedule(start_date=gm_dt, end_date=gm_dt, team=team_id, params=params)
            if not games:
                no_gm()
                time.sleep(60 * 240)  # check back 4 hours from now
            else:
                print(games[0])
                what_sleep=get_score()
                print(f"Sleeping {what_sleep} seconds")
                print(gc.mem_free())
                time.sleep(what_sleep)

except OSError as e:
    #https://github.com/espressif/esp-idf/issues/2907
    if 'MBEDTLS_ERR_SSL_CONN_EOF' in str(e):
        import machine
        machine.reset()
except Exception as e:
    print(sys.print_exception(e))
    myoled.text(str(e), 0, 0 )
    myoled.show()
    sys.exit(1)                    #Kill everything and hope we got a good error on the oled    
    