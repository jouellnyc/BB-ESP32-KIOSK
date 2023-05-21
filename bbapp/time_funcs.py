import time
import utime

"""
    We calculate the non-UTC local date (NULD) using 'timezone' to find out what 'today' is.
    We submit *that* date to MLB API to find the games for today and there start times (in UTC (z) )
    We convert *that* ('game_datetime': '2023-04-06T17:10:00Z') to NULT to display the upcoming game time
""" 

#EDT
timezone = -4
tz_name  = 'et'

""" Game Time to query  MLB API for game data using timezone in ntp_setup.py """
yr, mt, dy, hr, mn, *_ = [  f"{x:02d}" for x in utime.localtime(utime.mktime(utime.localtime()) + (int(timezone)*3600)) ]
gyr, gmt, gdy, ghr, gmn, *_ = [  f"{x:02d}" for x in utime.gmtime() ]

gm_dt  = f"{mt}/{dy}/{yr}"
gmm_dt = f"{gmt}/{gdy}/{gyr}"

short_yr = f"{int( str(yr)[2:]):02d}"

def game_day_now():
    yr, mt, dy, hr, mn, *_ = [  f"{x:02d}" for x in utime.localtime(utime.mktime(utime.localtime()) + (int(timezone)*3600)) ]
    return f"{yr}-{mt}-{dy}"

def utc_to_local(_time):
    
    _w=_time.replace(':','-').replace('T','-').replace('Z','').split('-')
    _w.append('0')
    _w.append('0')
    _w = [ int(x) for x in _w ]
    _w=tuple(_w)
    utc_time = time.mktime(_w)


    # Constants
    DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    # Get MicroPython UTC epoch time in seconds.
    utc_time = time.mktime(_w)
    # Offset UTC by timezone using 3600 seconds per hour.
    local_time = utc_time + 3600 * timezone
    # Get local time's datetime tuple.
    yy, mo, dd, hh, mm, ss, wkd, yrd = [d for d in time.localtime(local_time)]
    # Set the RTC to local time.  (I don't think the uP docs are exactly right about this.)

    if hh >= 13:
        am_pm = 'p'
        hh    = hh - 12
    elif hh == 12:
        #JJO noon should be pm
        am_pm = 'p'
    else:
        am_pm = 'a'
    then_time = '%2.2d-%2.2d %1.1d:%2.2d' % (mo, dd, hh, mm, ) + am_pm
    return then_time