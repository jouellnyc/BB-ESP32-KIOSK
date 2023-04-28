from hardware.ntp_setup import utc_to_local
gm={'doubleheader': 'N', 'away_pitcher_note': '', 'game_date': '2023-04-26', 'inning_state': 'Top', 'away_probable_pitcher': '', 'home_rec': '9-15', 'away_rec': '14-9', 'game_num': 1, 'game_datetime': '2023-04-26T16:35:00Z', 'current_inning': 1, 'game_type': 'R', 'away_score': 0, 'away_name': 'Texas Rangers', 'summary': '2023-04-26 - Texas Rangers @ Cincinnati Reds (Pre-Game)', 'away_id': 140, 'home_name': 'Cincinnati Reds', 'status': 'Pre-Game', 'venue_id': 2602, 'venue_name': 'Great American Ball Park', 'home_probable_pitcher': '', 'home_pitcher_note': '', 'home_score': 0, 'home_id': 113, 'game_id': 718424}
gm_time=gm.get('game_datetime','NA')
tm=utc_to_local(gm_time)
gm_time='2023-04-26T16:35:00Z'
utc_to_local(gm_time)
for h in range(0, 24):
    gm_time=f"2023-04-26T{h}:35:00Z"
    utc_to_local(gm_time)