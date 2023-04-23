import ujson

with open("/bbapp/team_ids.py") as f:
    at = ujson.loads(f.read())

for team in at['teams']:
    print(team)
    
    
from bbapp.team_colors import TEAM_COLORS
for t, c in sorted( TEAM_COLORS.items()):
    print(t, c)
    

for team in sorted(at['teams'], key=lambda d: d['teamCode']): 
    if team['teamCode'].upper() in TEAM_COLORS.keys():
        print(f"{team['teamCode'].upper()} OK")
    else:
        print(f"{team['teamCode'].upper()} NOTOK")