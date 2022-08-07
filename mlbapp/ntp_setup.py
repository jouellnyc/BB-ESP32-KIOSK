from machine import  RTC
import time
import ntptime

print("Local time before synchronization：%s" % str(time.localtime()))
ntptime.host = "time.google.com"
ntptime.settime()   # This sets the RTC to UTC.
print("Local time after synchronization：%s" % str(time.localtime()))


""" Credit 
https://github.com/the-stanely/Clock-ESP32-Nokia5110/blob/master/ESP32-5110-Clock.py
"""

#----------------------------------------------------------------------------------
# Mode of operation
timezone = -4
clockmode = 12  # 24 or 12
#----------------------------------------------------------------------------------

# Constants
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
# Get MicroPython UTC epoch time in seconds.
utc_time = time.time()
# Offset UTC by timezone using 3600 seconds per hour.
local_time = utc_time + 3600 * timezone
# Get local time's datetime tuple.
yy, mo, dd, hh, mm, ss, wkd, yrd = [d for d in time.localtime(local_time)]
# Set the RTC to local time.  (I don't think the uP docs are exactly right about this.)
RTC().datetime((yy, mo, dd, 0, hh, mm, ss, 0))
now = RTC().datetime()
now_day = str(DAYS[now[3]])[:3]
now_date = '%2.2d/%2.2d/%2.2d' % (now[1], now[2], now[0])
now_day_date = now_day + '. ' + now_date

now4 = now[4]
if clockmode == 24:
    am_pm = ''
else:
    if now[4] >= 13:
        am_pm = '  PM'
        now4 = now[4] - 12
    elif now[4] == 0:
        now4 = 12
    else:
        am_pm = '  AM'
        

def utc_to_local(_time):
    
    _w=_time.replace(':','-').replace('T','-').replace('Z','').split('-')
    _w.append('0')
    _w.append('0')
    _w = [ int(x) for x in _w ]
    _w=tuple(_w)
    utc_time = time.mktime(_w)


    timezone = -4
    clockmode = 12

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
    elif hh == 0:
        hh = 12
    else:
        am_pm = 'a'
            
    then_time = '%2.2d-%2.2d %1.1d:%2.2d' % (mo, dd, hh, mm, ) + am_pm
    return then_time

if __name__ == "__main__":
    main()