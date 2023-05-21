import time
import ujson

with open("/bbapp/team_ids.py") as f:
        all_teams = ujson.loads(f.read())

from hardware.screen_runner import display as d
from hardware.ili9341 import color565
from bbapp.team_colors import TEAM_COLORS
    
def show_teams():

    for team in all_teams['teams']:
        print(team)
    
    for t, c in sorted( TEAM_COLORS.items()):
        print(t, c)
        d.fresh_box()    
        r, g, b = c
        color = color565(r, g, b)
        d.draw_text(5, 100, f"{t}:5 "   , d.score_font, d.white , color)
        time.sleep(1)


def grep_team(letter):
    for team in all_teams['teams']:
        if letter in team['teamName']:
            c = TEAM_COLORS[team['teamCode'].upper()]
            r, g, b = c
            color = color565(r, g, b)
            team_code=team['teamCode'].upper()
            print(f"team_id={team['id']}")
            print(f"team_name='{team['teamName']}'")
            print(f"team_code='{team['teamCode'].upper()}'")
            print("")
            d.fresh_box()
            d.draw_text(5, 100, f"{team_code}:5", d.score_font, d.white , color)
            
"""
from bbapp.test_colors import grep_team, show_teams
grep_team('Car')
"""    
    
    