import ujson

with open("/bbapp/team_ids.py") as f:
        at = ujson.loads(f.read())
        
def show_teams():
    
    for team in at['teams']:
        print(team)
    
    from bbapp.team_colors import TEAM_COLORS
    for t, c in sorted( TEAM_COLORS.items()):
        print(t, c)

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
    