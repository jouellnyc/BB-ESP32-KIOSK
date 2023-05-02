import time
import ujson

with open("/bbapp/team_ids.py") as f:
        at = ujson.loads(f.read())
        
def show_teams():
    
    from hardware.screen_runner import display as d
    from hardware.ili9341 import color565

    for team in at['teams']:
        print(team)
    
    from bbapp.team_colors import TEAM_COLORS
    
    for t, c in sorted( TEAM_COLORS.items()):
        print(t, c)
        d.fresh_box()    
        r, g, b = c
        color = color565(r, g, b)
        d.draw_text(5, 100, f"{t}:5 "   , d.score_font, d.white , color)
        time.sleep(1)

def grep_team(letter):
    for team in at['teams']:
        if letter in team['teamName']:
            print(f"team_id={team['id']}")
            print(f"team_name='{team['teamName']}'")
            print(f"team_code='{team['teamCode'].upper()}'")
            print("")
            
"""
from bbapp.test_colors import grep_team
grep_team('Car')
"""    
    