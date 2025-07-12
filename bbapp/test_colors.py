import time
import ujson

# Configuration
TEAM_DATA_FILE = "/bbapp/team_ids.py"

# Import dependencies at module level
from bbapp.team_colors import TEAM_COLORS
from hardware.screen_runner import display as d
from hardware.ili9341 import color565

        
def show_all_teams():

    for team in load_teams_from_file():
        print(team)
    
    for t, c in sorted(TEAM_COLORS.items()):
        print(t, c)
        d.fresh_box()    
        r, g, b = c
        color = color565(r, g, b)
        d.draw_text(5, 100, f"{t}:5 "   , d.score_font, d.white , color)
        time.sleep(1)

def load_teams_from_file(filename=None):
    """Load teams data from JSON file - MicroPython compatible"""
    if filename is None:
        filename = TEAM_DATA_FILE
    try:
        with open(filename, 'r') as f:
            return ujson.load(f)
    except OSError:
        print("Error: File '{}' not found".format(filename))
        return None
    except ValueError:
        print("Error: Invalid JSON in file '{}'".format(filename))
        return None

def grep_team(search_term, filename=None, case_sensitive=False):
    """
    Search for teams by matching letters in various team fields.
    MicroPython compatible version.
    
    Args:
        search_term (str): Letters to search for
        filename (str): JSON file containing team data
        case_sensitive (bool): Whether search should be case sensitive
    
    Returns:
        list: List of matching team dictionaries
    """
    teams_data = load_teams_from_file(filename)
    if not teams_data:
        return []
    
    matches = []
    if not case_sensitive:
        search_term = search_term.lower()
    
    for team in teams_data['teams']:
        # Fields to search in
        searchable_fields = [
            team['name'],
            team['teamCode'],
            team['teamName'],
            team['locationName'],
            team['shortName']
        ]
        
        # Check if search term appears in any field
        found = False
        for field in searchable_fields:
            field_value = field.lower() if not case_sensitive else field
            if search_term in field_value:
                matches.append(team)
                found = True
                break  # Don't add the same team multiple times
        
        if found:
            continue
    
    return matches

def print_team_details(teams):
    """Pretty print team details - MicroPython compatible"""
    if not teams:
        print("No teams found matching the search criteria.")
        return
    
    for i, team in enumerate(teams):
        print("--- Match {} ---".format(i + 1))
        print("ID: {}".format(team['id']))
        print("Name: {}".format(team['name']))
        print("Team Code: {}".format(team['teamCode']))
        print("Team Name: {}".format(team['teamName']))
        print("Location: {}".format(team['locationName']))
        print("Short Name: {}".format(team['shortName']))
        print()

def search_and_display(search_term, filename=None, case_sensitive=False):
    """
    Convenience function that searches and displays results
    MicroPython compatible version.
    """
    matches = grep_team(search_term, filename, case_sensitive)
    print("Search results for '{}':".format(search_term))
    print_team_details(matches)
    return matches

def get_team_by_code(team_code, filename=None):
    """
    Get a specific team by its team code (exact match)
    Useful for your color display function
    """
    teams_data = load_teams_from_file(filename)
    if not teams_data:
        return None
    
    team_code_lower = team_code.lower()
    for team in teams_data['teams']:
        if team['teamCode'].lower() == team_code_lower:
            return team
    return None

def grep_team_with_colors(search_term):
    """
    Simplified function - imports are handled automatically
    
    Args:
        search_term: Letters to search for
    """
    matches = grep_team(search_term)
    
    for team in matches:
        team_code_upper = team['teamCode'].upper()
        if team_code_upper in TEAM_COLORS:
            c = TEAM_COLORS[team_code_upper]
            r, g, b = c
            color = color565(r, g, b)
            
            print("team_id={}".format(team['id']))
            print("team_name='{}'".format(team['teamName']))
            print("team_code='{}'".format(team_code_upper))
            print("")
            
            d.fresh_box()
            d.draw_text(5, 100, "{}:5".format(team_code_upper), 
                       d.score_font, d.white, color)

# Example usage:
grep_team_with_colors("bos")
